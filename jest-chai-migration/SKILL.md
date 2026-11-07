---
name: jest-chai-migration
description: Migration automatisée Jest → Chai avec règles de transformation sûres. Utilise ce skill quand tu dois convertir des tests Jest en Chai, migrer une suite de tests, ou standardiser le framework de test.
version: 1.0.0
intent_hash: 0xJEST_CHAI_MIGRATION_20260812
---

# Jest → Chai Migration

## Objectif

Migrer les tests Jest vers Chai avec des transformations sûres et réversibles.
Conserver la couverture de tests et la sémantique d'assertion.

## Déclencheur

- Migration d'un projet de Jest vers Chai
- Standardisation du framework de test
- Mise à jour de tests legacy
- Audit de dépendances de test

## Règles de transformation

### 1. `expect(...).toBe(...)` → `expect(...).to.equal(...)`

```javascript
// Jest
expect(result).toBe(42);

// Chai
expect(result).to.equal(42);
```

### 2. `expect(...).toEqual(...)` → `expect(...).to.deep.equal(...)`

```javascript
// Jest
expect(obj).toEqual({ a: 1 });

// Chai
expect(obj).to.deep.equal({ a: 1 });
```

### 3. `expect(...).toThrow(...)` → `expect(() => fn()).to.throw(...)`

```javascript
// Jest
expect(() => fn()).toThrow(Error);

// Chai
expect(() => fn()).to.throw(Error);
```

### 4. `beforeEach` / `afterEach` → inchangés

```javascript
// Identique Jest/Chai
beforeEach(() => { /* setup */ });
afterEach(() => { /* teardown */ });
```

### 5. `describe` / `it` → inchangés

```javascript
// Identique Jest/Chai
describe('suite', () => {
  it('test', () => { /* ... */ });
});
```

### 6. `jest.fn()` → `sinon.stub()` ou `chai.spy`

```javascript
// Jest
const mock = jest.fn();

// Chai + sinon
const mock = sinon.stub();

// OU chai-spies
const mock = chai.spy();
```

### 7. `jest.mock()` → `sinon.stub()` ou `proxyquire`

```javascript
// Jest
jest.mock('module', () => ({ ... }));

// Chai + sinon + proxyquire
const proxyquire = require('proxyquire');
const module = proxyquire('module', { /* stubs */ });
```

### 8. `toBeTruthy()` / `toBeFalsy()` → `to.be.true` / `to.be.false`

```javascript
// Jest
expect(val).toBeTruthy();
expect(val).toBeFalsy();

// Chai
expect(val).to.be.true;
expect(val).to.be.false;
```

### 9. `toBeNull()` → `to.be.null`

```javascript
// Jest
expect(val).toBeNull();

// Chai
expect(val).to.be.null;
```

### 10. `toHaveLength()` → `to.have.lengthOf()`

```javascript
// Jest
expect(arr).toHaveLength(3);

// Chai
expect(arr).to.have.lengthOf(3);
```

## Migration automatisée

```bash
# Exécuter la migration
npx jest-chai-migrate --src tests/ --dst tests/

# Dry-run
npx jest-chai-migrate --src tests/ --dry-run
```

## Validation

Après migration :
1. `npm test` doit passer
2. Couverture inchangée (`npm run test:coverage`)
3. Pas d'import `jest` restants

## Anti-patterns

- ❌ Migrer sans dry-run
- ❌ Supprimer des tests pendant la migration
- ❌ Changer la logique métier pendant la migration
- ❌ Oublier de mettre à jour `package.json`

## Référence ADR

- **ADR** : ADR-2026-08-09-PSL-PIANO-DIFF-Q243
- **IntentHash** : `0xJEST_CHAI_MIGRATION_20260812`
- **Dépôt** : gerivdb/GeriCode
