// One Excel workbook with every table except the large per-MP votes table.
import type { APIRoute } from "astro";
import ExcelJS from "exceljs";
import { tables } from "../../lib/opendata";
export const GET: APIRoute = async () => {
  const wb = new ExcelJS.Workbook(); wb.creator = "faktickapoznamka.sk"; wb.created = new Date();
  for (const t of tables().filter((x) => !x.file.startsWith("hlasy-"))) {
    const ws = wb.addWorksheet(t.title.slice(0, 31), { views: [{ state: "frozen", ySplit: 1 }] });
    ws.columns = t.cols.map(([key, label]) => ({ header: label, key, width: Math.min(60, Math.max(10, label.length + 2)) }));
    ws.getRow(1).font = { bold: true };
    for (const r of t.rows) ws.addRow(r);
    ws.autoFilter = { from: { row: 1, column: 1 }, to: { row: 1, column: t.cols.length } };
  }
  const info = wb.addWorksheet("O dátach");
  info.addRows([["faktickapoznamka.sk – otvorené dáta o NR SR"], ["Zdroj: oficiálne záznamy Národnej rady SR (nrsr.sk)."], ["Licencia spracovania: CC BY 4.0, uveďte zdroj faktickapoznamka.sk."], [`Vytvorené: ${new Date().toISOString().slice(0, 10)}`]]);
  const buf = await wb.xlsx.writeBuffer();
  return new Response(buf as ArrayBuffer, { headers: { "content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" } });
};
