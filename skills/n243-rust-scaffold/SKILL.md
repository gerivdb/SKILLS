---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xN243_RUST_SCAFFOLD_20260801
status: active
---

# Skill: n243-rust-scaffold

## Purpose
Generate Rust scaffold for N243 meta-engine (243 dispatch slots).

## Action
1. Read designs/n243-meta-engine.design.yaml
2. Generate src/n243/dispatch.rs with 243 slot enum
3. Generate src/n243/kernel/*.rs stubs per slot
4. Generate Cargo.toml with zig build dependency

## Verify
cargo check -> clean compile

## Ref
D-012: n243-meta-engine.design.yaml
