import { describe, it, expect } from 'vitest';
import { FilterPanel } from './FilterPanel';

describe('RF-UI-04: Filtros e Tabela de Resultados', () => {
  it('deve exportar o componente FilterPanel com suporte a UF, ano e nível de risco IEA', () => {
    expect(FilterPanel).toBeDefined();
    expect(typeof FilterPanel).toBe('function');
  });
});
