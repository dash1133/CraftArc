import { DIFFERENCE } from "@/content/copy";
import FormVsDialogueVisual from "../visuals/FormVsDialogueVisual";

export default function FormsVsConversationSection() {
  const t = DIFFERENCE.table;
  return (
    <section id="difference" className="bg-white">
      <div className="mx-auto max-w-[1200px] px-5 py-20 sm:px-8 sm:py-24">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-ink-2">{DIFFERENCE.eyebrow}</p>
        <h2 className="mt-3 max-w-[760px] text-3xl font-semibold tracking-tight sm:text-4xl">{DIFFERENCE.h2}</h2>
        <p className="mt-3 max-w-[680px] text-ink-2">{DIFFERENCE.sub}</p>
        <div className="mt-10"><FormVsDialogueVisual /></div>
        <div className="mt-10 overflow-x-auto rounded-xl border border-slate-200">
          <table className="w-full min-w-[620px] text-left text-[14.5px]">
            <thead className="bg-canvas text-xs uppercase tracking-wide text-ink-2">
              <tr>{t.head.map((h, i) => <th key={i} scope="col" className="px-4 py-3 font-semibold">{h}</th>)}</tr>
            </thead>
            <tbody>
              {t.rows.map((r) => (
                <tr key={r[0]} className="border-t border-slate-200">
                  <th scope="row" className="px-4 py-3 font-medium text-ink">{r[0]}</th>
                  <td className="px-4 py-3 text-ink-2">{r[1]}</td>
                  <td className="px-4 py-3 font-medium text-ink">{r[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
