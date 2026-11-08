import { describe, it, expect } from 'vitest';
import { NetworkGraph } from './NetworkGraph';

describe('RF-UI-02: Visualizador Interativo Cytoscape.js', () => {
  it('deve exportar o componente NetworkGraph para renderização da rede', () => {
    expect(NetworkGraph).toBeDefined();
    expect(typeof NetworkGraph).toBe('function');
  });
});
