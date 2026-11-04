/**
 * @fileoverview m3-notebook-workspace-registrar - Google Apps Script
 * Ajoute automatiquement toute nouvelle conversation NotebookLM au workspace cible.
 * Premier relais après m3-omni-notebook-bridge dans la chaine OMNI-INTER-NOTEBOOK-LM.
 */

/**
 * Constantes de configuration
 */
const CONFIG = {
  TARGET_WORKSPACE_ID: 'GERICODE_3_TARGET',
  GATEWAY_URL: 'http://127.0.0.1:18000/mcp/gateway-manager',
  REGISTRY_SHEET_ID: '', // ID du Google Sheet registre des liens conversation-workspace
  LOG_SHEET_ID: ''       // ID du Google Sheet journal des opérations
};

/**
 * Point d'entrée déclenché par la création d'une nouvelle conversation NotebookLM.
 * Appelé par le déclencheur Google Apps Script sur l'événement onCreate.
 *
 * @param {Object} e - Événement de déclenchement NotebookLM
 */
function onNotebookCreated(e) {
  try {
    const notebookId = e.notebookId || e.parameter.notebook_id;
    const title = e.title || e.parameter.title || 'Untitled';
    const createdAt = e.createdAt || new Date().toISOString();
    const author = e.author || Session.getEffectiveUser().getEmail();
    
    Logger.log('[m3-notebook-workspace-registrar] Nouvelle conversation détectée: ' + notebookId);
    
    // 1. Vérifier que la conversation existe et est accessible
    if (!notebookExists(notebookId)) {
      Logger.log('[ERROR] Conversation non trouvée: ' + notebookId);
      return { status: 'error', message: 'Conversation non trouvée: ' + notebookId };
    }
    
    // 2. Vérifier que la conversation n'est pas déjà dans le workspace cible
    if (isAlreadyInWorkspace(notebookId, CONFIG.TARGET_WORKSPACE_ID)) {
      Logger.log('[INFO] Conversation déjà dans le workspace: ' + notebookId);
      return { status: 'duplicate', message: 'Conversation déjà dans le workspace cible' };
    }
    
    // 3. Ajouter la conversation au workspace cible
    const addResult = addNotebookToWorkspace(notebookId, CONFIG.TARGET_WORKSPACE_ID);
    if (!addResult.success) {
      Logger.log('[ERROR] Échec ajout workspace: ' + addResult.error);
      return { status: 'error', message: addResult.error };
    }
    
    // 4. Mettre à jour le registre des liens conversation-workspace
    updateRegistry(notebookId, CONFIG.TARGET_WORKSPACE_ID, 'active');
    
    // 5. Mettre à jour le node M3-Tree via le gateway-manager
    const m3Result = notifyM3Tree(notebookId, title, created_at, CONFIG.TARGET_WORKSPACE_ID);
    
    // 6. Journalisation
    logOperation(notebookId, CONFIG.TARGET_WORKSPACE_ID, 'added', 'success');
    
    return {
      status: 'success',
      notebook_id: notebookId,
      workspace_id: CONFIG.TARGET_WORKSPACE_ID,
      m3_node_id: m3Result.node_id || null,
      edges_created: m3Result.edges_created || 0
    };
    
  } catch (error) {
    Logger.log('[ERROR] Exception dans onNotebookCreated: ' + error.toString());
    return { status: 'error', message: error.toString() };
  }
}

/**
 * Vérifie si une conversation NotebookLM existe et est accessible.
 *
 * @param {string} notebookId - Identifiant de la conversation
 * @return {boolean} true si la conversation existe et est accessible
 */
function notebookExists(notebookId) {
  try {
    // Tentative d'accès à la conversation via l'API Apps Script NotebookLM
    // (à adapter selon l'API réelle disponible)
    var url = 'https://notebooklm.google.com/v1/notebooks/' + encodeURIComponent(notebookId);
    var response = UrlFetchApp.fetch(url, {
      method: 'GET',
      muteHttpExceptions: true
    });
    return response.getResponseCode() === 200;
  } catch (e) {
    Logger.log('[ERROR] Erreur vérification existence: ' + e.toString());
    return false;
  }
}

/**
 * Vérifie si une conversation est déjà associée à un workspace cible.
 *
 * @param {string} notebookId - Identifiant de la conversation
 * @param {string} workspaceId - Identifiant du workspace cible
 * @return {boolean} true si déjà associé
 */
function isAlreadyInWorkspace(notebookId, workspaceId) {
  try {
    var sheet = SpreadsheetApp.openById(CONFIG.REGISTRY_SHEET_ID);
    var sheet = sheet.getSheetByName('conversation_workspace_links');
    var data = sheet.getDataRange().getValues();
    
    for (var i = 1; i < data.length; i++) {
      if (data[i][0] === notebookId && data[i][1] === workspaceId) {
        return true;
      }
    }
    return false;
  } catch (e) {
    Logger.log('[WARN] Impossible de vérifier le registre: ' + e.toString());
    return false;
  }
}

/**
 * Ajoute une conversation au workspace cible via l'API NotebookLM.
 *
 * @param {string} notebookId - Identifiant de la conversation
 * @param {string} workspaceId - Identifiant du workspace cible
 * @return {Object} Résultat de l'opération
 */
function addNotebookToWorkspace(notebookId, workspaceId) {
  try {
    var url = 'https://notebooklm.google.com/v1/workspaces/' + encodeURIComponent(workspaceId) + '/conversations/' + encodeURIComponent(notebookId);
    var response = UrlFetchApp.fetch(url, {
      method: 'POST',
      muteHttpExceptions: true,
      contentType: 'application/json'
    });
    
    if (response.getResponseCode() === 200 || response.getResponseCode() === 201) {
      return { success: true, message: 'Conversation ajoutée au workspace' };
    } else {
      return { success: false, error: 'Code HTTP: ' + response.getResponseCode() + ' - ' + response.getContentText() };
    }
  } catch (e) {
    return { success: false, error: e.toString() };
  }
}

/**
 * Met à jour le registre des liens conversation-workspace.
 *
 * @param {string} notebookId - Identifiant de la conversation
 * @param {string} workspaceId - Identifiant du workspace cible
 * @param {string} status - Statut du lien (active, inactive, archived)
 */
function updateRegistry(notebookId, workspaceId, status) {
  try {
    var sheet = SpreadsheetApp.openById(CONFIG.REGISTRY_SHEET_ID);
    var sheet = sheet.getSheetByName('conversation_workspace_links');
    var lastRow = sheet.getLastRow() + 1;
    
    sheet.getRange(lastRow, 1).setValue(notebookId);
    sheet.getRange(lastRow, 2).setValue(workspaceId);
    sheet.getRange(lastRow, 3).setValue(status);
    sheet.getRange(lastRow, 4).setValue(new Date().toISOString());
    
    Logger.log('[INFO] Registre mis à jour: ' + notebookId + ' -> ' + workspaceId);
  } catch (e) {
    Logger.log('[WARN] Impossible de mettre à jour le registre: ' + e.toString());
  }
}

/**
 * Notifie le gateway-manager (port 18000) pour créer le node M3-Tree.
 *
 * @param {string} notebookId - Identifiant de la conversation
 * @param {string} title - Titre de la conversation
 * @param {string} createdAt - Horodatage de création
 * @param {string} targetWorkspaceId - Identifiant du workspace cible
 * @return {Object} Résultat de la création du node
 */
function notifyM3Tree(notebookId, title, createdAt, targetWorkspaceId) {
  try {
    var payload = {
      jsonrpc: '2.0',
      method: 'tools/call',
      params: {
        name: 'preflight_import',
        arguments: {
          notebook_id: notebookId,
          title: title,
          created_at: createdAt,
          target_workspace_id: targetWorkspaceId,
          linked_conversation_ids: []
        }
      },
      id: 1
    };
    
    var response = UrlFetchApp.fetch(CONFIG.GATEWAY_URL, {
      method: 'POST',
      muteHttpExceptions: true,
      contentType: 'application/json',
      payload: JSON.stringify(payload)
    });
    
    if (response.getResponseCode() === 200) {
      var result = JSON.parse(response.getContentText());
      return result.result || {};
    } else {
      Logger.log('[WARN] Échec notification M3-Tree: ' + response.getResponseCode());
      return { node_id: null, edges_created: 0 };
    }
  } catch (e) {
    Logger.log('[WARN] Impossible de contacter le gateway-manager: ' + e.toString());
    return { node_id: null, edges_created: 0 };
  }
}

/**
 * Journalise une opération d'ajout de conversation.
 *
 * @param {string} notebookId - Identifiant de la conversation
 * @param {string} workspaceId - Identifiant du workspace cible
 * @param {string} action - Action effectuée (added, removed, updated)
 * @param {string} status - Statut de l'opération (success, error)
 */
function logOperation(notebookId, workspaceId, action, status) {
  try {
    var sheet = SpreadsheetApp.openById(CONFIG.LOG_SHEET_ID);
    var sheet = sheet.getSheetByName('operation_log');
    var lastRow = sheet.getLastRow() + 1;
    
    sheet.getRange(lastRow, 1).setValue(new Date().toISOString());
    sheet.getRange(lastRow, 2).setValue(notebookId);
    sheet.getRange(lastRow, 3).setValue(workspaceId);
    sheet.getRange(lastRow, 4).setValue(action);
    sheet.getRange(lastRow, 5).setValue(status);
    
  } catch (e) {
    Logger.log('[WARN] Impossible d'écrire le log: ' + e.toString());
  }
}

/**
 * Fonction de test pour valider le script sans déclencheur réel.
 *
 * @return {Object} Résultat du test
 */
function testNotebookRegistration() {
  var testResult = onNotebookCreated({
    notebookId: 'test_notebook_001',
    title: 'Test Conversation',
    createdAt: new Date().toISOString(),
    author: 'test_user'
  });
  Logger.log(JSON.stringify(testResult));
  return testResult;
}
