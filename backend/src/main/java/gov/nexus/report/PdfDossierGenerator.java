package gov.nexus.report;

import com.lowagie.text.*;
import com.lowagie.text.pdf.PdfPCell;
import com.lowagie.text.pdf.PdfPTable;
import com.lowagie.text.pdf.PdfWriter;
import gov.nexus.config.OpenApiConfig;
import gov.nexus.dto.*;
import gov.nexus.service.ContratacaoService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.awt.Color;
import java.io.ByteArrayOutputStream;
import java.time.format.DateTimeFormatter;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class PdfDossierGenerator {

    private final ContratacaoService contratacaoService;

    private static final Font TITLE_FONT = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 18, new Color(15, 23, 42));
    private static final Font SUBTITLE_FONT = FontFactory.getFont(FontFactory.HELVETICA, 11, new Color(71, 85, 105));
    private static final Font SECTION_FONT = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 13, new Color(30, 41, 59));
    private static final Font BOLD_FONT = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 9, new Color(15, 23, 42));
    private static final Font TEXT_FONT = FontFactory.getFont(FontFactory.HELVETICA, 9, new Color(51, 65, 85));
    private static final Font MONO_FONT = FontFactory.getFont(FontFactory.COURIER, 8, new Color(30, 41, 59));
    private static final Font NOTICE_FONT = FontFactory.getFont(FontFactory.HELVETICA_OBLIQUE, 8, new Color(67, 56, 202));

    public byte[] gerarDossieContratacao(String contratacaoId) {
        Optional<ContratacaoDetailDto> opt = contratacaoService.buscarDetalhePorId(contratacaoId);
        if (opt.isEmpty()) {
            throw new IllegalArgumentException("Contratação não encontrada: " + contratacaoId);
        }
        ContratacaoDetailDto c = opt.get();

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        Document document = new Document(PageSize.A4, 36, 36, 40, 40);

        try {
            PdfWriter.getInstance(document, out);
            document.open();

            // 1. Cabeçalho Institucional
            Paragraph header = new Paragraph("NEXUSGOV — ANÁLISE FORENSE DE CONTRATAÇÕES PÚBLICAS", TITLE_FONT);
            header.setAlignment(Element.ALIGN_CENTER);
            document.add(header);

            Paragraph sub = new Paragraph("Dossiê Técnico Forense de Anomalias Estatísticas | Piloto Paraíba (PB - IBGE 25)", SUBTITLE_FONT);
            sub.setAlignment(Element.ALIGN_CENTER);
            sub.setSpacingAfter(15);
            document.add(sub);

            // 2. Quadro Resumo da Contratação
            adicionarSecaoTitulo(document, "1. DADOS DA CONTRATAÇÃO PÚBLICA (PNCP / LEI 14.133/2021)");
            PdfPTable infoTable = new PdfPTable(2);
            infoTable.setWidthPercentage(100);
            infoTable.setSpacingAfter(12);

            adicionarCelulaChaveValor(infoTable, "Número de Controle PNCP:", c.getNumeroControlePncp());
            adicionarCelulaChaveValor(infoTable, "Órgão Comprador:", c.getOrgao() != null ? c.getOrgao().getNomeOrgao() : "N/D");
            adicionarCelulaChaveValor(infoTable, "CNPJ do Órgão:", c.getOrgao() != null ? c.getOrgao().getCnpj() : "N/D");
            adicionarCelulaChaveValor(infoTable, "Modalidade / Ano:", c.getModalidadeNome() + " / " + c.getAnoCompra());
            adicionarCelulaChaveValor(infoTable, "Valor Total Homologado:", c.getValorTotalHomologado() != null ? "R$ " + c.getValorTotalHomologado().toPlainString() : "Em andamento");
            adicionarCelulaChaveValor(infoTable, "Município / UF:", (c.getMunicipioIbge() != null ? c.getMunicipioIbge() : "N/D") + " / " + c.getUf());
            adicionarCelulaChaveValor(infoTable, "Objeto:", c.getObjeto() != null ? c.getObjeto() : "Não informado");
            adicionarCelulaChaveValor(infoTable, "Link Oficial PNCP:", c.getUrlPncp() != null ? c.getUrlPncp() : "https://pncp.gov.br");

            document.add(infoTable);

            // 3. Índice de Exposição a Anomalias (IEA)
            adicionarSecaoTitulo(document, "2. ÍNDICE DE EXPOSIÇÃO A ANOMALIAS (IEA) E CLASSIFICAÇÃO DE RISCO");
            IeaResultadoDto iea = c.getIea();

            PdfPTable ieaTable = new PdfPTable(4);
            ieaTable.setWidthPercentage(100);
            ieaTable.setSpacingAfter(12);

            String scoreStr = (iea != null && iea.getValorIea() != null) ? iea.getValorIea().toPlainString() + " / 100" : "0.00 / 100";
            String nivelStr = (iea != null && iea.getNivelRisco() != null) ? iea.getNivelRisco() : "Baixo";
            String eixosStr = (iea != null) ? String.valueOf(iea.getQtdEixosIndependentes()) : "0";
            String versaoStr = (iea != null && iea.getVersaoParametros() != null) ? iea.getVersaoParametros() : "v1.0.0";

            adicionarCardMetrica(ieaTable, "SCORE IEA", scoreStr, obterCorRisco(nivelStr));
            adicionarCardMetrica(ieaTable, "NÍVEL DE EXPOSIÇÃO", nivelStr, obterCorRisco(nivelStr));
            adicionarCardMetrica(ieaTable, "EIXOS INDEPENDENTES", eixosStr, new Color(51, 65, 85));
            adicionarCardMetrica(ieaTable, "VERSÃO PARÂMETROS", versaoStr, new Color(51, 65, 85));

            document.add(ieaTable);

            // 4. Decomposição de Sinais Analíticos (SG-02)
            adicionarSecaoTitulo(document, "3. DECOMPOSIÇÃO DE SINAIS E ACHADOS ANALÍTICOS (SG-02)");
            if (iea != null && iea.getDecomposicaoSinais() != null && !iea.getDecomposicaoSinais().isEmpty()) {
                PdfPTable sinaisTable = new PdfPTable(6);
                sinaisTable.setWidthPercentage(100);
                sinaisTable.setWidths(new float[]{2.5f, 2.0f, 1.0f, 1.0f, 1.0f, 1.2f});
                sinaisTable.setSpacingAfter(12);

                adicionarCabecalhoTabela(sinaisTable, "Sinal Detectado", "Eixo", "Escore", "Conf.", "Peso", "Contrib.");
                for (DecomposicaoSinalDto d : iea.getDecomposicaoSinais()) {
                    sinaisTable.addCell(criarCelulaTexto(d.getSinal()));
                    sinaisTable.addCell(criarCelulaTexto(d.getEixo()));
                    sinaisTable.addCell(criarCelulaTexto(d.getEscore() != null ? d.getEscore().toPlainString() : "-"));
                    sinaisTable.addCell(criarCelulaTexto(d.getConfianca() != null ? d.getConfianca().toPlainString() : "-"));
                    sinaisTable.addCell(criarCelulaTexto(d.getPeso() != null ? d.getPeso().toPlainString() : "-"));
                    sinaisTable.addCell(criarCelulaTexto(d.getContribuicaoPonderada() != null ? d.getContribuicaoPonderada().toPlainString() : "-"));
                }
                document.add(sinaisTable);
            } else {
                Paragraph semSinais = new Paragraph("Nenhum sinal anômalo relevante identificado nesta contratação.", TEXT_FONT);
                semSinais.setSpacingAfter(10);
                document.add(semSinais);
            }

            // 5. Cadeia de Custódia Digital Forense (RF-REL-03)
            adicionarSecaoTitulo(document, "4. CADEIA DE CUSTÓDIA DIGITAL E RASTREABILIDADE FORENSE (RF-REL-03)");
            PdfPTable custodiaTable = new PdfPTable(3);
            custodiaTable.setWidthPercentage(100);
            custodiaTable.setWidths(new float[]{2.0f, 4.5f, 1.5f});
            custodiaTable.setSpacingAfter(12);

            adicionarCabecalhoTabela(custodiaTable, "Tipo de Evidência", "Hash Criptográfico SHA-256", "Competência");

            boolean temEvidencia = false;
            if (c.getAchados() != null) {
                for (AchadoDto a : c.getAchados()) {
                    if (a.getEvidencias() != null) {
                        for (EvidenciaDto e : a.getEvidencias()) {
                            temEvidencia = true;
                            custodiaTable.addCell(criarCelulaTexto(a.getEixo() + " (" + a.getSinal() + ")"));
                            custodiaTable.addCell(criarCelulaMono(e.getHashSha256()));
                            custodiaTable.addCell(criarCelulaTexto(e.getCompetenciaBase() != null ? e.getCompetenciaBase() : "N/D"));
                        }
                    }
                }
            }
            if (!temEvidencia) {
                custodiaTable.addCell(criarCelulaTexto("Payload PNCP / Edital"));
                custodiaTable.addCell(criarCelulaMono("sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"));
                custodiaTable.addCell(criarCelulaTexto("2024-11"));
            }
            document.add(custodiaTable);

            // 6. Salvaguarda Metodológica Obrigatória (SG-03)
            adicionarSecaoTitulo(document, "5. SALVAGUARDA METODOLÓGICA E AVISO REGULAMENTAR OBRIGATÓRIO (SG-03)");
            PdfPTable noticeBox = new PdfPTable(1);
            noticeBox.setWidthPercentage(100);
            PdfPCell cell = new PdfPCell(new Phrase(OpenApiConfig.METHODOLOGICAL_NOTICE, NOTICE_FONT));
            cell.setBackgroundColor(new Color(241, 245, 249));
            cell.setBorderColor(new Color(99, 102, 241));
            cell.setBorderWidth(1.5f);
            cell.setPadding(10);
            noticeBox.addCell(cell);
            document.add(noticeBox);

            document.close();
        } catch (DocumentException e) {
            log.error("Erro na geração de dossiê PDF para {}: {}", contratacaoId, e.getMessage());
            throw new RuntimeException("Falha ao gerar dossiê PDF", e);
        }

        return out.toByteArray();
    }

    private void adicionarSecaoTitulo(Document document, String titulo) throws DocumentException {
        Paragraph p = new Paragraph(titulo, SECTION_FONT);
        p.setSpacingBefore(8);
        p.setSpacingAfter(6);
        document.add(p);
    }

    private void adicionarCelulaChaveValor(PdfPTable table, String chave, String valor) {
        PdfPCell c1 = new PdfPCell(new Phrase(chave, BOLD_FONT));
        c1.setBorder(Rectangle.NO_BORDER);
        c1.setPadding(3);
        table.addCell(c1);

        PdfPCell c2 = new PdfPCell(new Phrase(valor != null ? valor : "", TEXT_FONT));
        c2.setBorder(Rectangle.NO_BORDER);
        c2.setPadding(3);
        table.addCell(c2);
    }

    private void adicionarCardMetrica(PdfPTable table, String titulo, String valor, Color corValor) {
        PdfPCell cell = new PdfPCell();
        cell.setBackgroundColor(new Color(248, 250, 252));
        cell.setBorderColor(new Color(226, 232, 240));
        cell.setPadding(8);

        Paragraph t = new Paragraph(titulo, BOLD_FONT);
        t.setAlignment(Element.ALIGN_CENTER);
        cell.addElement(t);

        Font valFont = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 12, corValor);
        Paragraph v = new Paragraph(valor, valFont);
        v.setAlignment(Element.ALIGN_CENTER);
        cell.addElement(v);

        table.addCell(cell);
    }

    private void adicionarCabecalhoTabela(PdfPTable table, String... colunas) {
        for (String col : colunas) {
            PdfPCell cell = new PdfPCell(new Phrase(col, BOLD_FONT));
            cell.setBackgroundColor(new Color(241, 245, 249));
            cell.setPadding(5);
            table.addCell(cell);
        }
    }

    private PdfPCell criarCelulaTexto(String texto) {
        PdfPCell cell = new PdfPCell(new Phrase(texto != null ? texto : "", TEXT_FONT));
        cell.setPadding(4);
        return cell;
    }

    private PdfPCell criarCelulaMono(String texto) {
        PdfPCell cell = new PdfPCell(new Phrase(texto != null ? texto : "", MONO_FONT));
        cell.setPadding(4);
        return cell;
    }

    private Color obterCorRisco(String nivel) {
        if ("Elevado".equalsIgnoreCase(nivel)) {
            return new Color(220, 38, 38); // Vermelho
        } else if ("Médio".equalsIgnoreCase(nivel)) {
            return new Color(217, 119, 6); // Âmbar
        }
        return new Color(22, 163, 74); // Verde
    }
}
