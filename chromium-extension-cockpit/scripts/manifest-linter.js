#!/usr/bin/env node
// -*- coding: utf-8 -*-
// manifest-linter.js — Linter statique pré-commit pour manifests MV3.
// Valide :
//   1. L'existence physique de 100% des fichiers référencés dans manifest.json
//   2. L'absence de directives dépréciées (focus-without-user-activation)
//   3. La validité des règles net_request.json (pas d'ID étranger dans initiatorDomains)
// Retourne code 0 si tout est valide, 1 sinon.

const fs = require("fs");
const path = require("path");

let errors = 0;

function error(msg) {
    console.error(`[LINT-ERROR] ${msg}`);
    errors++;
}

function warn(msg) {
    console.warn(`[LINT-WARN] ${msg}`);
}

function lintManifest(manifestPath) {
    const dir = path.dirname(manifestPath);
    let manifest;
    try {
        manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    } catch (e) {
        error(`manifest.json invalide (JSON) : ${e.message}`);
        return;
    }

    // --- Vérifier background service_worker ---
    if (manifest.background && manifest.background.service_worker) {
        const sw = path.join(dir, manifest.background.service_worker);
        if (!fs.existsSync(sw)) error(`Background service_worker manquant : ${manifest.background.service_worker}`);
    }

    // --- Vérifier side_panel ---
    if (manifest.side_panel && manifest.side_panel.default_path) {
        const sp = path.join(dir, manifest.side_panel.default_path);
        if (!fs.existsSync(sp)) error(`Side panel manquant : ${manifest.side_panel.default_path}`);
    }

    // --- Vérifier content_scripts ---
    if (manifest.content_scripts && Array.isArray(manifest.content_scripts)) {
        manifest.content_scripts.forEach((cs, i) => {
            if (cs.js && Array.isArray(cs.js)) {
                cs.js.forEach(f => {
                    const fp = path.join(dir, f);
                    if (!fs.existsSync(fp)) error(`content_scripts[${i}] js manquant : ${f}`);
                });
            }
            if (cs.css && Array.isArray(cs.css)) {
                cs.css.forEach(f => {
                    const fp = path.join(dir, f);
                    if (!fs.existsSync(fp)) error(`content_scripts[${i}] css manquant : ${f}`);
                });
            }
        });
    }

    // --- Vérifier web_accessible_resources ---
    if (manifest.web_accessible_resources && Array.isArray(manifest.web_accessible_resources)) {
        manifest.web_accessible_resources.forEach((res, i) => {
            if (res.resources && Array.isArray(res.resources)) {
                res.resources.forEach(f => {
                    const fp = path.join(dir, f);
                    if (!fs.existsSync(fp)) error(`web_accessible_resources[${i}] manquant : ${f}`);
                });
            }
        });
    }

    // --- Vérifier declarative_net_request ---
    if (manifest.declarative_net_request && manifest.declarative_net_request.rule_resources) {
        manifest.declarative_net_request.rule_resources.forEach((rr, i) => {
            if (rr.path) {
                const fp = path.join(dir, rr.path);
                if (!fs.existsSync(fp)) error(`DNR rule_resources[${i}] manquant : ${rr.path}`);
            }
        });
    }

    // --- Vérifier options_ui ---
    if (manifest.options_ui && manifest.options_ui.page) {
        const op = path.join(dir, manifest.options_ui.page);
        if (!fs.existsSync(op)) error(`options_ui.page manquant : ${manifest.options_ui.page}`);
    }

    // --- Vérifier action.default_popup ---
    if (manifest.action && manifest.action.default_popup) {
        const pp = path.join(dir, manifest.action.default_popup);
        if (!fs.existsSync(pp)) error(`action.default_popup manquant : ${manifest.action.default_popup}`);
    }
}

function lintDeprecatedDirectives(rootDir) {
    // Rechercher focus-without-user-activation dans tous les fichiers HTML
    const htmlFiles = [];
    function walk(dir) {
        for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
            const full = path.join(dir, entry.name);
            if (entry.isDirectory()) walk(full);
            else if (entry.name.endsWith(".html")) htmlFiles.push(full);
        }
    }
    walk(rootDir);

    htmlFiles.forEach(f => {
        const content = fs.readFileSync(f, "utf8");
        if (/focus-without-user-activation/.test(content)) {
            error(`Directive dépréciée 'focus-without-user-activation' trouvée dans ${path.relative(rootDir, f)}`);
        }
    });
}

function lintDNRRules(rootDir) {
    // Vérifier net_request.json pour les initiatorDomains avec ID étranger
    const dnrPath = path.join(rootDir, "net_request.json");
    if (!fs.existsSync(dnrPath)) return;
    try {
        const dnr = JSON.parse(fs.readFileSync(dnrPath, "utf8"));
        if (Array.isArray(dnr)) {
            dnr.forEach((rule, i) => {
                if (rule.condition && rule.condition.initiatorDomains) {
                    const ids = rule.condition.initiatorDomains;
                    const foreign = ids.filter(d => d && d.length > 40 && d !== "chrome-extension://");
                    if (foreign.length > 0) {
                        error(`net_request.json règle[${i}] : initiatorDomains contient des IDs étrangers : ${foreign.join(", ")}`);
                    }
                }
            });
        }
    } catch (e) {
        error(`net_request.json invalide (JSON) : ${e.message}`);
    }
}

function main() {
    const manifestPath = process.argv[2] || path.join(process.cwd(), "manifest.json");
    const rootDir = path.dirname(path.resolve(manifestPath));

    if (!fs.existsSync(manifestPath)) {
        error(`manifest.json introuvable : ${manifestPath}`);
        process.exit(1);
    }

    lintManifest(manifestPath);
    lintDeprecatedDirectives(rootDir);
    lintDNRRules(rootDir);

    if (errors === 0) {
        console.log("[LINT-OK] Manifest MV3 valide — aucun fichier fantôme, aucune directive dépréciée, DNR cohérent.");
        process.exit(0);
    } else {
        console.error(`[LINT-FAIL] ${errors} erreur(s) détectée(s).`);
        process.exit(1);
    }
}

main();
