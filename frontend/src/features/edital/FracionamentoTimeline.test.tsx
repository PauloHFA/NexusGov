import { describe, it, expect } from 'vitest';
import { FracionamentoTimeline } from './FracionamentoTimeline';

describe('RF-UI-05: Linha do Tempo de Fracionamento de Despesa', () => {
  it('deve exportar o componente FracionamentoTimeline', () => {
    expect(FracionamentoTimeline).toBeDefined();
    expect(typeof FracionamentoTimeline).toBe('function');
  });
});
