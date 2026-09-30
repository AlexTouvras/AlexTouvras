"use client";

import { useMemo, useState } from "react";
import type { DirectiveArchive, DirectiveItem } from "@/lib/directive-types";

function unique(values: string[]): string[] {
  return [...new Set(values.filter(Boolean))].sort();
}

function repoName(repo: string): string {
  return repo.split("/").pop() || repo;
}

export function DirectiveArchiveBrowser({ archive }: { archive: DirectiveArchive }) {
  const [query, setQuery] = useState("");
  const [repo, setRepo] = useState("");
  const [topic, setTopic] = useState("");
  const [kind, setKind] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const repos = useMemo(() => unique(archive.items.map((item) => item.repo)), [archive.items]);
  const topics = useMemo(
    () => unique(archive.items.flatMap((item) => item.topics)),
    [archive.items],
  );
  const kinds = useMemo(() => unique(archive.items.map((item) => item.kind)), [archive.items]);

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    return archive.items.filter((item) => {
      if (repo && item.repo !== repo) return false;
      if (topic && !item.topics.includes(topic)) return false;
      if (kind && item.kind !== kind) return false;
      if (!q) return true;
      const haystack = [item.title, item.repo, item.sourcePath, ...item.topics]
        .join(" ")
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [archive.items, query, repo, topic, kind]);

  const selected: DirectiveItem | undefined =
    archive.items.find((item) => item.id === selectedId) ?? visible[0];

  const budgets = useMemo(() => {
    const buckets = new Map<string, number>();
    for (const item of archive.items) {
      if (item.activation !== "always") continue;
      buckets.set(item.repo, (buckets.get(item.repo) ?? 0) + item.tokens);
    }
    return [...buckets.entries()]
      .map(([name, tokens]) => ({
        repo: name,
        tokens,
        over: tokens > archive.alwaysOnTokenCap,
      }))
      .sort((a, b) => b.tokens - a.tokens);
  }, [archive.items, archive.alwaysOnTokenCap]);

  return (
    <div>
      <p className="text-sm text-slate-400">
        Private snapshot from {archive.sourceRepo}
        {archive.sourceBranch ? ` (${archive.sourceBranch})` : ""} on {archive.publishedAt}.
        Always-on budget is {archive.alwaysOnTokenCap} tokens. This page does not publish
        directives onto the public site.
      </p>

      <div className="mt-4 flex flex-wrap gap-2">
        {budgets.map((budget) => (
          <button
            key={budget.repo}
            type="button"
            onClick={() => setRepo(budget.repo)}
            className={
              budget.over
                ? "rounded-full border border-rose-400/40 bg-rose-400/10 px-3 py-1 text-xs text-rose-200"
                : "rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-200"
            }
          >
            {repoName(budget.repo)} {budget.tokens} / {archive.alwaysOnTokenCap}
          </button>
        ))}
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <label className="text-xs uppercase tracking-wide text-slate-500">
          Search
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Title, repo, path"
            className="mt-1 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm normal-case tracking-normal text-white"
          />
        </label>
        <label className="text-xs uppercase tracking-wide text-slate-500">
          Repo
          <select
            value={repo}
            onChange={(event) => setRepo(event.target.value)}
            className="mt-1 w-full rounded-xl border border-white/10 bg-slate-950 px-3 py-2 text-sm normal-case tracking-normal text-white"
          >
            <option value="">All</option>
            {repos.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label className="text-xs uppercase tracking-wide text-slate-500">
          Topic
          <select
            value={topic}
            onChange={(event) => setTopic(event.target.value)}
            className="mt-1 w-full rounded-xl border border-white/10 bg-slate-950 px-3 py-2 text-sm normal-case tracking-normal text-white"
          >
            <option value="">All</option>
            {topics.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label className="text-xs uppercase tracking-wide text-slate-500">
          Kind
          <select
            value={kind}
            onChange={(event) => setKind(event.target.value)}
            className="mt-1 w-full rounded-xl border border-white/10 bg-slate-950 px-3 py-2 text-sm normal-case tracking-normal text-white"
          >
            <option value="">All</option>
            {kinds.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-[280px_1fr]">
        <ul className="max-h-[70vh] space-y-2 overflow-auto pr-1">
          {visible.length === 0 && (
            <li className="text-sm text-slate-400">Nothing matches these filters.</li>
          )}
          {visible.map((item) => (
            <li key={item.id}>
              <button
                type="button"
                onClick={() => setSelectedId(item.id)}
                className={
                  selected?.id === item.id
                    ? "w-full rounded-xl border border-neon-cyan/50 bg-white/10 p-3 text-left"
                    : "w-full rounded-xl border border-white/10 bg-white/5 p-3 text-left hover:bg-white/10"
                }
              >
                <span className="block font-medium text-white">{item.title}</span>
                <span className="mt-1 block text-xs text-slate-400">
                  {repoName(item.repo)} · {item.kind} · {item.activation} · {item.tokens} tokens
                </span>
              </button>
            </li>
          ))}
        </ul>

        {selected && (
          <article className="glass rounded-2xl p-5">
            <h2 className="text-xl font-medium text-white">{selected.title}</h2>
            <p className="mt-1 text-sm text-slate-400">
              {selected.tokens} tokens · {selected.kind} · {selected.activation}
              {selected.sourcePath ? ` · ${selected.sourcePath}` : ""}
            </p>
            <p className="mt-2 text-xs text-slate-500">{selected.topics.join(", ")}</p>
            {selected.sourceUrl && (
              <a
                href={selected.sourceUrl}
                className="mt-3 inline-block text-sm text-neon-cyan hover:underline"
              >
                Source
              </a>
            )}
            <pre className="mt-4 max-h-[60vh] overflow-auto whitespace-pre-wrap font-mono text-xs leading-relaxed text-slate-200">
              {selected.body}
            </pre>
          </article>
        )}
      </div>
    </div>
  );
}
