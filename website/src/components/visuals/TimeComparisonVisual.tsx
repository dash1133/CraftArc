/** Without the time: a review-season week full of blocked days, against one 25-minute conversation. */
export default function TimeComparisonVisual() {
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
  const blocked = [[0, 1, 2], [0, 1], [1, 2, 3], [0, 2, 3], [0, 1, 2, 3]];
  return (
    <div data-sample className="grid grid-cols-2 gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div>
        <p className="mb-2 text-[11px] font-medium text-ink-2">Traditional Review Season</p>
        <div className="grid grid-cols-5 gap-1">
          {days.map((d, i) => (
            <div key={d} className="space-y-1">
              <p className="text-center text-[10px] text-ink-2">{d}</p>
              {[0, 1, 2, 3].map((slot) => (
                <div key={slot} className={`h-3.5 rounded-sm ${blocked[i].includes(slot) ? "bg-red-200" : "bg-slate-100"}`} />
              ))}
            </div>
          ))}
        </div>
      </div>
      <div>
        <p className="mb-2 text-[11px] font-medium text-ink-2">CraftArc Agent</p>
        <div className="grid grid-cols-5 gap-1">
          {days.map((d, i) => (
            <div key={d} className="space-y-1">
              <p className="text-center text-[10px] text-ink-2">{d}</p>
              {[0, 1, 2, 3].map((slot) => (
                <div key={slot} className={`h-3.5 rounded-sm ${i === 2 && slot === 1 ? "bg-emerald-400" : "bg-slate-100"}`} />
              ))}
            </div>
          ))}
        </div>
        <p className="tabular mt-2 inline-flex rounded-full bg-emerald-50 px-2 py-0.5 text-[11px] font-medium text-emerald-700 ring-1 ring-inset ring-emerald-200">25 min, voice or text</p>
      </div>
    </div>
  );
}
