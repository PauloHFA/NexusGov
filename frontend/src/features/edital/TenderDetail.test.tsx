import { describe, it, expect } from 'vitest';
import { TenderDetail } from './TenderDetail';

describe('RF-UI-03: Ficha de Detalhe da Contratação com IEA', () => {
  it('deve exportar o componente TenderDetail para exibição de IEA e decomposição de sinais', () => {
    expect(TenderDetail).toBeDefined();
    expect(typeof TenderDetail).toBe('function');
  });
});
