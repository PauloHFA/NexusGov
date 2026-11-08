import { describe, it, expect } from 'vitest';
import React from 'react';
import { renderToString } from 'react-dom/server';
import { AuditCopilotModal } from './AuditCopilotModal';

describe('Melhoria 3: AuditCopilotModal', () => {
  it('deve renderizar modal quando aberto com identificação do processo e salvaguardas', () => {
    const html = renderToString(
      <AuditCopilotModal
        isOpen={true}
        onClose={() => {}}
        contratacaoId="c-100"
        numeroControlePncp="08778268000160-1-000001/2024"
        orgaoNome="Prefeitura de João Pessoa"
        ieaScore={65.4}
        nivelRisco="Elevado"
      />
    );

    expect(html).toContain('NexusGov Audit Copilot');
    expect(html).toContain('08778268000160-1-000001/2024');
    expect(html).toContain('65.4');
    expect(html).toContain('SG-01 Validada');
    expect(html).toContain('Gerar Minuta com Copilot');
  });

  it('não deve renderizar conteúdo quando isOpen=false', () => {
    const html = renderToString(
      <AuditCopilotModal
        isOpen={false}
        onClose={() => {}}
        contratacaoId="c-100"
        numeroControlePncp="08778268000160-1-000001/2024"
        orgaoNome="Prefeitura de João Pessoa"
        ieaScore={65.4}
        nivelRisco="Elevado"
      />
    );

    expect(html).toBe('');
  });
});
