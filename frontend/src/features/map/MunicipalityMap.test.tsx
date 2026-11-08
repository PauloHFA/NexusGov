import { describe, it, expect } from 'vitest';
import React from 'react';
import { renderToString } from 'react-dom/server';
import { MunicipalityMap } from './MunicipalityMap';

describe('RF-UI-06 / CA-UI-06: Visão Agregada Territorial e Mapa Municipal', () => {
  it('deve renderizar a listagem de municípios da Paraíba sem expor dados pessoais', () => {
    const html = renderToString(<MunicipalityMap />);

    expect(html).toContain('Distribuição Territorial de Exposição — Piloto Paraíba (PB)');
    expect(html).toContain('João Pessoa');
    expect(html).toContain('Campina Grande');
    expect(html).toContain('Patos');
    expect(html).toContain('2507507'); // Código IBGE João Pessoa
    expect(html).toContain('2504009'); // Código IBGE Campina Grande

    // Garante ausência de dados pessoais (PII) per LGPD
    expect(html).not.toContain('***.***.***-**');
    expect(html).not.toContain('CPF');
  });

  it('deve formatar indicadores de IEA médio e contagem de processos', () => {
    const html = renderToString(<MunicipalityMap />);

    expect(html).toContain('IEA Médio');
    expect(html).toContain('contratações analisadas');
  });
});
