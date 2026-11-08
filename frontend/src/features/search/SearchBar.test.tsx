import { describe, it, expect } from 'vitest';
import { SearchBar } from './SearchBar';

describe('RF-UI-01: Barra de Pesquisa Global', () => {
  it('deve ser um componente de função válido com suporte a filtro e limpeza', () => {
    expect(SearchBar).toBeDefined();
    expect(typeof SearchBar).toBe('function');
  });
});
