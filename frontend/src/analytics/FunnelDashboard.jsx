import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { GlassCard } from "components/ui";
import { useAuth } from "contexts/AuthContext";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000/api";

const FunnelDashboard = () => {
  const { getAccessToken } = useAuth();
  const [data, setData] = useState({ funnel: [], totals: {} });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/analytics/funnel/`, {
          headers: { Authorization: `Bearer ${getAccessToken()}` },
        });
        setData(response.data);
      } catch (err) {
        setError("Unable to load analytics. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [getAccessToken]);

  const totals = useMemo(() => data.totals || {}, [data.totals]);

  return (
    <div className="min-h-screen bg-[color:var(--bg-color,#f8fafc)] px-4 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <header className="space-y-2">
          <h1 className="text-3xl font-bold text-[color:var(--accent,#111827)]">Exercise Analytics</h1>
          <p className="text-sm text-[color:var(--muted-text,#6b7280)]">
            Track how learners move through exercises and where they request help.
          </p>
        </header>

        {loading && (
          <GlassCard padding="lg" className="text-sm text-[color:var(--muted-text,#6b7280)]">
            Loading analytics...
          </GlassCard>
        )}

        {error && !loading && (
          <GlassCard padding="lg" className="border-[color:var(--error,#dc2626)]/40 bg-[color:var(--error,#dc2626)]/10 text-[color:var(--error,#dc2626)]">
            {error}
          </GlassCard>
        )}

        {!loading && !error && (
          <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
            <GlassCard padding="lg" className="overflow-hidden">
              <div className="flex items-center justify-between border-b border-[color:var(--border-color,#d1d5db)] pb-4">
                <h2 className="text-lg font-semibold text-[color:var(--accent,#111827)]">Per-exercise funnel</h2>
                <span className="text-xs font-semibold uppercase tracking-wide text-[color:var(--muted-text,#6b7280)]">
                  Session totals: {totals.starts || 0} starts
                </span>
              </div>

              <div className="mt-4 overflow-x-auto">
                <table className="min-w-full divide-y divide-[color:var(--border-color,#d1d5db)] text-sm">
                  <thead>
                    <tr className="text-left text-[color:var(--muted-text,#6b7280)]">
                      <th className="px-4 py-2 font-semibold">Exercise</th>
                      <th className="px-4 py-2 font-semibold">Starts</th>
                      <th className="px-4 py-2 font-semibold">Hints</th>
                      <th className="px-4 py-2 font-semibold">Errors</th>
                      <th className="px-4 py-2 font-semibold">Completions</th>
                      <th className="px-4 py-2 font-semibold">Conversion</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[color:var(--border-color,#d1d5db)]">
                    {data.funnel?.map((row) => {
                      const completionRate = row.starts
                        ? Math.round(((row.completions || 0) / row.starts) * 100)
                        : 0;
                      return (
                        <tr key={row.exercise_id}>
                          <td className="px-4 py-3 font-medium text-[color:var(--accent,#111827)]">
                            Exercise {row.exercise_id || "-"}
                          </td>
                          <td className="px-4 py-3">{row.starts}</td>
                          <td className="px-4 py-3">{row.hints}</td>
                          <td className="px-4 py-3">{row.errors}</td>
                          <td className="px-4 py-3">{row.completions}</td>
                          <td className="px-4 py-3 font-semibold">{completionRate}%</td>
                        </tr>
                      );
                    })}
                    {data.funnel?.length === 0 && (
                      <tr>
                        <td
                          className="px-4 py-4 text-center text-[color:var(--muted-text,#6b7280)]"
                          colSpan={6}
                        >
                          No events recorded yet.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </GlassCard>

            <GlassCard padding="lg" className="space-y-3">
              <h2 className="text-lg font-semibold text-[color:var(--accent,#111827)]">Totals</h2>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <MetricCard label="Starts" value={totals.starts || 0} />
                <MetricCard label="Hints" value={totals.hints || 0} />
                <MetricCard label="Errors" value={totals.errors || 0} />
                <MetricCard label="Completions" value={totals.completions || 0} />
              </div>
            </GlassCard>
          </div>
        )}
      </div>
    </div>
  );
};

const MetricCard = ({ label, value }) => (
  <div className="rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-[color:var(--bg-color,#f8fafc)] px-4 py-4 text-center">
    <div className="text-xs font-semibold uppercase tracking-wide text-[color:var(--muted-text,#6b7280)]">{label}</div>
    <div className="text-xl font-bold text-[color:var(--accent,#111827)]">{value}</div>
  </div>
);

export default FunnelDashboard;
