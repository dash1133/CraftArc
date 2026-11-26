"use client";

import { useRef, useState } from "react";
import {
  Bar, BarChart, CartesianGrid, Cell, Legend as RLegend, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";
import { BOARD } from "@/content/copy";
import {
  boardTabs, cohortFlow, competencies, gapToTarget, leverCombos, levers, managingOut, partnersOnEmerging, trajectory, trajectoryKpi,
} from "@/content/sampleDashboard";
import { SampleBadge, StatusTag } from "../visuals/ui";

const C = { above: "#10B981", at: "#3B82F6", below: "#F59E0B", risk: "#EF4444", ink: "#0F172A", grid: "#E2E8F0", muted: "#475569" };
const axis = { fontSize: 12, fill: C.muted };
const legendText = (v: string) => <span style={{ color: C.muted }}>{v}</span>;

export default function BoardDashboardSection() {
  const [tab, setTab] = useState(0);
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const onKey = (e: React.KeyboardEvent, i: number) => {
    const n = boardTabs.length;
    let next = -1;
    if (e.key === "ArrowRight") next = (i + 1) % n;
    if (e.key === "ArrowLeft") next = (i - 1 + n) % n;
    if (next >= 0) { e.preventDefault(); setTab(next); refs.current[next]?.focus(); }
  };

  return (
    <section id="board" className="bg-white">
      <span id="cockpit" data-anchor aria-hidden="true" />
      <div className="mx-auto max-w-[1200px] px-5 py-20 sm:px-8 sm:py-24">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-ink-2">{BOARD.eyebrow}</p>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">{BOARD.h2}</h2>
          <SampleBadge label={BOARD.sampleBadge} />
          <StatusTag>{BOARD.status}</StatusTag>
        </div>

        <div data-sample className="mt-8 overflow-hidden rounded-2xl border border-slate-200">
          <div className="border-b border-slate-200 bg-canvas p-5 sm:p-6">
            <p className="text-xs font-semibold uppercase tracking-[0.14em] text-ink-2">{BOARD.insightLabel}</p>
            <p className="mt-2 max-w-[900px] font-serif text-2xl leading-snug text-ink sm:text-[1.7rem]">{BOARD.insight}</p>
          </div>
          <div role="tablist" aria-label="Board view sections" className="flex overflow-x-auto border-b border-slate-200">
            {boardTabs.map((t, i) => (
              <button
                key={t.id}
                ref={(el) => { refs.current[i] = el; }}
                id={`tab-${t.id}`}
                role="tab"
                type="button"
                aria-selected={tab === i}
                aria-controls={`panel-${t.id}`}
                tabIndex={tab === i ? 0 : -1}
                onClick={() => setTab(i)}
                onKeyDown={(e) => onKey(e, i)}
                className={`whitespace-nowrap border-b-2 px-4 py-3 text-sm font-medium transition sm:px-5 ${tab === i ? "border-ink text-ink" : "border-transparent text-ink-2 hover:text-ink"}`}
              >
                {t.label}
              </button>
            ))}
          </div>
          {boardTabs.map((t, i) => (
            <div key={t.id} id={`panel-${t.id}`} role="tabpanel" aria-labelledby={`tab-${t.id}`} hidden={tab !== i} className="grid grid-cols-1 gap-6 p-5 sm:p-6 lg:grid-cols-12">
              <div className="lg:col-span-4">
                <p className="text-sm text-ink-2">{t.question}</p>
                <h3 className="mt-3 text-xl font-semibold tracking-tight">{t.headline}</h3>
                <p className="mt-2 text-[15px] leading-relaxed text-ink-2">{t.body}</p>
              </div>
              <div className="min-h-[300px] lg:col-span-8">{tab === i && <Panel id={t.id} />}</div>
            </div>
          ))}
        </div>
        <p className="mt-4 max-w-[900px] text-xs leading-relaxed text-ink-2">{BOARD.footnote}</p>
      </div>
    </section>
  );
}

function Box({ children, h = 300 }: { children: React.ReactElement; h?: number }) {
  return <div style={{ width: "100%", height: h }}><ResponsiveContainer width="100%" height="100%">{children}</ResponsiveContainer></div>;
}

function Panel({ id }: { id: string }) {
  if (id === "gap") {
    return (
      <Box>
        <BarChart data={gapToTarget} layout="vertical" margin={{ left: 8, right: 16, top: 8, bottom: 8 }} barSize={26}>
          <CartesianGrid horizontal={false} stroke={C.grid} />
          <XAxis type="number" domain={[0, 100]} unit="%" tick={axis} />
          <YAxis type="category" dataKey="level" tick={axis} width={80} />
          <Tooltip formatter={(v) => `${v}%`} />
          <RLegend wrapperStyle={{ fontSize: 12 }} formatter={legendText} />
          <Bar dataKey="below" name="Below target" stackId="a" fill={C.below} />
          <Bar dataKey="at" name="At target" stackId="a" fill={C.at} />
          <Bar dataKey="above" name="Above target (ready for next level)" stackId="a" fill={C.above} />
        </BarChart>
      </Box>
    );
  }
  if (id === "trajectory") {
    const flow = [
      { k: "Moved up", v: cohortFlow.movedUp, c: "bg-above" },
      { k: "Stayed below", v: cohortFlow.stayedBelow, c: "bg-below" },
      { k: "Left", v: cohortFlow.left, c: "bg-slate-400" },
    ];
    return (
      <div className="grid grid-cols-1 gap-5 md:grid-cols-5">
        <div className="md:col-span-3">
          <Box h={240}>
            <LineChart data={trajectory} margin={{ left: 0, right: 16, top: 12, bottom: 4 }}>
              <CartesianGrid vertical={false} stroke={C.grid} />
              <XAxis dataKey="year" tick={axis} />
              <YAxis domain={[40, 100]} unit="%" tick={axis} width={44} />
              <Tooltip formatter={(v) => `${v}%`} />
              <ReferenceLine x="FY24" stroke={C.muted} strokeDasharray="3 3" label={{ value: "Targets raised", fontSize: 11, fill: C.muted, position: "insideTopRight" }} />
              <Line type="monotone" dataKey="pct" name="At or above target" stroke={C.ink} strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </Box>
        </div>
        <div className="space-y-4 md:col-span-2">
          <div className="rounded-xl border border-slate-200 p-4">
            <p className="tabular text-4xl font-semibold">{trajectoryKpi.value}</p>
            <p className="text-sm text-ink-2">{trajectoryKpi.label}</p>
            <p className="tabular mt-1 text-sm font-medium text-emerald-700">{trajectoryKpi.delta}</p>
          </div>
          <div className="rounded-xl border border-slate-200 p-4">
            <p className="tabular text-sm text-ink-2">Last year&apos;s {cohortFlow.total} below target</p>
            <div className="mt-2 flex h-3 overflow-hidden rounded-full">
              {flow.map((f) => <span key={f.k} className={f.c} style={{ width: `${(f.v / cohortFlow.total) * 100}%` }} />)}
            </div>
            <ul className="tabular mt-2 space-y-0.5 text-sm">
              {flow.map((f) => <li key={f.k} className="flex justify-between"><span className="text-ink-2">{f.k}</span><span className="font-medium">{f.v}</span></li>)}
            </ul>
          </div>
        </div>
      </div>
    );
  }
  if (id === "competencies") {
    return (
      <div>
        <Box h={280}>
          <BarChart data={competencies} layout="vertical" margin={{ left: 8, right: 24, top: 8, bottom: 8 }} barSize={16}>
            <CartesianGrid horizontal={false} stroke={C.grid} />
            <XAxis type="number" domain={[0, 40]} unit="%" tick={axis} />
            <YAxis type="category" dataKey="name" tick={axis} width={130} />
            <Tooltip formatter={(v) => `${v}% below target`} />
            <Bar dataKey="below" name="Below target">
              {competencies.map((c) => <Cell key={c.name} fill={c.kind === "Emerging" ? C.below : C.at} />)}
            </Bar>
          </BarChart>
        </Box>
        <div className="mt-2 flex flex-wrap gap-4 text-xs text-ink-2">
          <span className="inline-flex items-center gap-1.5"><span className="h-2 w-2 rounded-sm bg-on" />Traditional</span>
          <span className="inline-flex items-center gap-1.5"><span className="h-2 w-2 rounded-sm bg-below" />Emerging</span>
          <span className="tabular ml-auto">Partners at or above target on emerging: <strong className="text-ink">{partnersOnEmerging}%</strong></span>
        </div>
      </div>
    );
  }
  if (id === "managing-out") {
    const nonReg = managingOut.exits.reduce((a, e) => a + e.nonRegretted, 0);
    const reg = managingOut.exits.reduce((a, e) => a + e.regretted, 0);
    return (
      <div className="grid grid-cols-1 gap-5 md:grid-cols-5">
        <div className="grid grid-cols-1 gap-3 md:col-span-2">
          <Metric value={`${managingOut.longBelow}`} label="below target for 3+ years" note={`${managingOut.noAction} with no action recorded`} tone="text-red-700" />
          <Metric value={`${managingOut.medianMonths} mo`} label="median time to a decision" />
          <Metric value={`${nonReg} : ${reg}`} label="non-regretted to regretted exits, five years" />
        </div>
        <div className="md:col-span-3">
          <Box h={260}>
            <BarChart data={managingOut.exits} margin={{ left: 0, right: 8, top: 8, bottom: 4 }} barSize={28}>
              <CartesianGrid vertical={false} stroke={C.grid} />
              <XAxis dataKey="year" tick={axis} />
              <YAxis allowDecimals={false} tick={axis} width={28} />
              <Tooltip />
              <RLegend wrapperStyle={{ fontSize: 12 }} formatter={legendText} />
              <Bar dataKey="nonRegretted" name="Non-regretted exits" stackId="x" fill={C.at} />
              <Bar dataKey="regretted" name="Regretted exits" stackId="x" fill={C.risk} />
            </BarChart>
          </Box>
        </div>
      </div>
    );
  }
  return (
    <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
      <div>
        <p className="mb-1 text-xs font-medium text-ink-2">Share of hours and growth, by lever</p>
        <Box h={260}>
          <BarChart data={levers} margin={{ left: 0, right: 8, top: 8, bottom: 4 }} barGap={2}>
            <CartesianGrid vertical={false} stroke={C.grid} />
            <XAxis dataKey="lever" tick={{ ...axis, fontSize: 11 }} interval={0} />
            <YAxis tick={axis} width={28} />
            <Tooltip />
            <RLegend wrapperStyle={{ fontSize: 12 }} formatter={legendText} />
            <Bar dataKey="hours" name="% of hours" fill="#CBD5E1" />
            <Bar dataKey="growth" name="Growth (pts)" fill={C.above} />
          </BarChart>
        </Box>
      </div>
      <div>
        <p className="mb-1 text-xs font-medium text-ink-2">Growth by number of levers used (pts)</p>
        <Box h={260}>
          <BarChart data={leverCombos} margin={{ left: 0, right: 8, top: 8, bottom: 4 }} barSize={36}>
            <CartesianGrid vertical={false} stroke={C.grid} />
            <XAxis dataKey="levers" tick={axis} />
            <YAxis tick={axis} width={28} />
            <Tooltip />
            <Bar dataKey="growth" name="Growth (pts)">
              {leverCombos.map((l, i) => <Cell key={l.levers} fill={i === leverCombos.length - 1 ? C.above : "#94A3B8"} />)}
            </Bar>
          </BarChart>
        </Box>
      </div>
    </div>
  );
}

function Metric({ value, label, note, tone = "text-ink" }: { value: string; label: string; note?: string; tone?: string }) {
  return (
    <div className="rounded-xl border border-slate-200 p-4">
      <p className={`tabular text-3xl font-semibold ${tone}`}>{value}</p>
      <p className="text-sm text-ink-2">{label}</p>
      {note && <p className="mt-1 text-xs font-medium text-red-700">{note}</p>}
    </div>
  );
}
