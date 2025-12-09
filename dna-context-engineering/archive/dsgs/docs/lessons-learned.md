# Lessons Learned from McpAdapter and TemplateEvolver Refactoring

## 1. TypeScript Type System Challenges

### Problem
Encountered "Argument of type 'never'" errors when trying to mock ConstraintGenerator methods in tests.

### Solution
- Avoid using type assertions (as any) as they bypass type safety
- Ensure mock functions are properly typed and defined in the correct scope
- Use module-level mocks with proper export/import handling

### Best Practice
```typescript
// Correct way to mock a module
jest.mock('../../src/core/constraint/ConstraintGenerator', () => {
  const mockGenerateConstraints = jest.fn();
  return {
    ConstraintGenerator: jest.fn().mockImplementation(() => {
      return {
        generateConstraints: mockGenerateConstraints
      };
    }),
    generateConstraints: mockGenerateConstraints
  };
});
```

## 2. Module Import/Export Issues

### Problem
McpAdapter was importing generateConstraints function directly, but ConstraintGenerator had been refactored to use class methods.

### Solution
- Update imports to match the current module exports
- Use class instantiation with proper dependency injection
- Handle dynamic imports for circular dependency scenarios

### Best Practice
```typescript
// Use class instantiation with dependencies
const templateMatcher = new (await import('../../core/constraint/TemplateMatcher')).TemplateMatcher();
const templateScorer = new (await import('../../core/constraint/TemplateScorer')).TemplateScorer();
const constraintGenerator = new ConstraintGenerator(templateMatcher, templateScorer);
```

## 3. Test Dependency Management

### Problem
Mock functions were not available in the test scope due to improper jest.mock usage.

### Solution
- Define mock functions at the module level
- Ensure mock functions are exported from the mocked module
- Use require() to access mocked functions when needed

### Best Practice
```typescript
// Define mock at module level
const mockGenerateConstraints = require('../../src/core/constraint/ConstraintGenerator').generateConstraints;

// Use in beforeEach
beforeEach(() => {
  mockGenerateConstraints.mockReset();
  mockGenerateConstraints.mockResolvedValue([/* test data */]);
});
```

## 4. Systematic Problem Solving

### Problem
Initial approach of fixing one error at a time led to "whack-a-mole" debugging.

### Solution
- Analyze the entire call chain and dependency graph
- Implement comprehensive fixes that address root causes
- Verify all related tests pass after changes

### Best Practice
1. Understand the full architecture and data flow
2. Identify all related components and their interactions
3. Implement coordinated changes across all affected files
4. Run comprehensive tests to verify the solution

## 5. TemplateEvolver Logic Improvements

### Problem
Historical effectiveness was being reset incorrectly when there were no outcomes.

### Solution
- Preserve the previous effectiveness value when there are no outcomes
- Avoid resetting to a default value which loses historical context

### Best Practice
```typescript
// Preserve historical effectiveness when no outcomes
if (totalOutcomes > 0) {
  metrics.historicalEffectiveness = metrics.resolutions / totalOutcomes;
} else {
  // Keep previous value to maintain historical context
  metrics.historicalEffectiveness = metrics.historicalEffectiveness;
}
```

## 6. General Development Principles

1. **Understand the Architecture**: Before making changes, understand the overall system design and component relationships.

2. **Comprehensive Solutions**: Address root causes rather than symptoms, and implement coordinated changes across related components.

3. **Type Safety**: Respect TypeScript's type system and avoid bypassing it with type assertions.

4. **Proper Mocking**: Use jest.mock correctly, understanding its scoping rules and the difference between named and default exports.

5. **Thorough Testing**: Verify that all relevant tests pass after changes, not just the ones directly related to the immediate problem.

6. **Documentation**: Document lessons learned to prevent repeating the same mistakes in future development.
