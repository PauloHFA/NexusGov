import { describe, it, expect } from 'vitest';
import { METHODOLOGICAL_TEXT } from './MethodologicalNotice';

describe('RF-UI-07 / SG-03: Aviso Metodológico Obrigatório', () => {
  it('deve conter menção expressa à Resolução TCU nº 367/2024 e presunção de inocência', () => {
    expect(METHODOLOGICAL_TEXT).toContain('Resolução TCU nº 367/2024');
    expect(METHODOLOGICAL_TEXT).toContain('Art. 19-B');
    expect(METHODOLOGICAL_TEXT).toContain('contraditório e a ampla defesa');
  });

  it('deve respeitar a salvaguarda SG-01 não contendo termos acusatórios proibidos', () => {
    const forbidden = ['fraude', 'crime', 'culpado', 'conluio comprovado'];
    for (const term of forbidden) {
      expect(METHODOLOGICAL_TEXT.toLowerCase()).not.toContain(term);
    }
  });
});
