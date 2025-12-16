import React from "react";
import { useNavigate } from "react-router-dom";
import {
  Award,
  BarChartLine,
  ChatDots,
  Compass,
  Lightning,
  Robot,
  Trophy,
} from "react-bootstrap-icons";
import Header from "components/layout/Header";
import { GlassCard, GlassButton } from "components/ui";
import logo from "assets/logo/monevo-logo-png.png";
import mockup1 from "assets/mobile-1.png";
import mockup2 from "assets/mobile-2.png";
import mockup3 from "assets/mobile-3.png";

const highlights = [
  {
    title: "5-minute lessons",
    description: "Short videos, quizzes, and budget drills you can finish on a break.",
    icon: <Lightning className="h-5 w-5" />,
  },
  {
    title: "Gamified momentum",
    description: "Earn badges, streaks, and leaderboard cred as you level up.",
    icon: <Trophy className="h-5 w-5" />,
  },
  {
    title: "AI tutor on call",
    description: "Ask anything and get simple, actionable guidance 24/7.",
    icon: <Robot className="h-5 w-5" />,
  },
];

const valueProps = [
  {
    title: "Micro-lessons that fit your day",
    text: "Complete structured 5-minute missions with instant feedback and practice tasks.",
    badge: "Bite-sized",
  },
  {
    title: "Personalized learning paths",
    text: "Follow tracks for basics, budgeting, investing, crypto, and real estate with adaptive recommendations.",
    badge: "Custom",
  },
  {
    title: "Finance tools built in",
    text: "Use calculators, converters, planners, and portfolio trackers while you learn.",
    badge: "Hands-on",
  },
  {
    title: "Rewards that keep you coming back",
    text: "Unlock badges, streaks, quests, and community leaderboards to stay motivated.",
    badge: "Motivating",
  },
];

const featureSections = [
  {
    icon: <Robot size={56} className="text-[color:var(--primary,#1d5330)]" />,
    title: "AI Finance Assistant",
    text: "24/7 chat mentor that breaks down any topic, explains calculations, and turns confusion into clarity.",
    mockup: mockup1,
    bullets: ["Guided answers tailored to your goals", "Real-time examples with market context", "Instant study notes & summaries"],
  },
  {
    icon: <Compass size={56} className="text-[color:var(--primary,#1d5330)]" />,
    title: "Personalized Learning Paths",
    text: "Choose a track and progress through quests that adapt as you advance.",
    mockup: mockup2,
    bullets: ["Tracks for basics, budgeting, investing, crypto, real estate", "Adaptive recommendations after each mission", "Progress bars and streak counters"],
  },
  {
    icon: <Trophy size={56} className="text-[color:var(--primary,#1d5330)]" />,
    title: "Gamified Learning",
    text: "Earn rewards for every action—quizzes, streaks, and challenges all count toward your next badge.",
    mockup: mockup3,
    bullets: ["Daily streaks and XP ladders", "Leaderboards with friends and cohorts", "Special quests like Budget Boss & Debt Destroyer"],
  },
];

const stats = [
  { label: "Avg. daily streak", value: "12 days" },
  { label: "Lessons completed", value: "125K+" },
  { label: "Badges earned", value: "480K" },
  { label: "Community rating", value: "4.8/5" },
];

const lessonTypes = [
  { title: "Video & audio", detail: "Crisp explainers with timestamps you can replay." },
  { title: "Interactive drills", detail: "Drag-and-drop, calculators, and practice sliders." },
  { title: "Quizzes & scenarios", detail: "MCQs, numeric inputs, and real-world prompts." },
  { title: "Action plans", detail: "Mini budgets, payoff plans, and investing checklists." },
];

function Welcome() {
  const navigate = useNavigate();

  return (
    <div className="app-container min-h-screen flex flex-col bg-[color:var(--bg-color,#ffffff)] text-[color:var(--text-color,#111827)]">
      <Header />

      <main className="relative flex-1 pt-[90px]">
        <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute -left-24 top-0 h-80 w-80 rounded-full bg-emerald-300/20 blur-3xl" />
          <div className="absolute bottom-10 right-0 h-72 w-72 rounded-full bg-sky-200/25 blur-3xl" />
          <div className="absolute left-1/2 top-32 h-48 w-48 -translate-x-1/2 rounded-full bg-[color:var(--primary,#1d5330)]/15 blur-3xl" />
          <div className="absolute left-6 top-1/3 h-36 w-36 rotate-12 rounded-3xl border border-emerald-200/60 bg-white/40 shadow-xl backdrop-blur-xl" />
          <div className="absolute right-10 top-24 h-32 w-32 -rotate-6 rounded-3xl border border-sky-200/60 bg-white/40 shadow-xl backdrop-blur-xl" />
        </div>

        <div className="mx-auto flex w-full max-w-6xl flex-col gap-16 px-4 py-12 sm:px-6 lg:px-8">
          <section className="relative grid gap-10 overflow-hidden rounded-3xl border border-[color:var(--border-color,#d1d5db)] bg-white/80 p-8 shadow-2xl shadow-[color:var(--primary,#1d5330)]/10 backdrop-blur-xl lg:grid-cols-[1.1fr_0.9fr] lg:p-12">
            <div className="absolute inset-0 -z-10 bg-gradient-to-br from-emerald-50 via-white to-sky-50" aria-hidden />
            <div className="absolute right-6 top-6 inline-flex items-center gap-2 rounded-full bg-emerald-100/70 px-4 py-2 text-xs font-semibold text-[color:var(--primary,#1d5330)] shadow-sm">
              <Lightning className="h-4 w-4" />
              New interactive welcome
            </div>

            <div className="space-y-6 text-left">
              <div className="flex items-center gap-3 rounded-full bg-white/70 px-4 py-2 shadow-sm w-fit">
                <img src={logo} alt="Monevo logo" className="h-8 w-auto" loading="lazy" />
                <span className="text-sm font-semibold text-[color:var(--text-color,#111827)]">Monevo Personal Finance Lab</span>
              </div>
              <div className="inline-flex items-center gap-2 rounded-full bg-[color:var(--primary,#1d5330)]/10 px-4 py-2 text-xs font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">
                Master your money, one level at a time
              </div>
              <h1 className="text-4xl font-bold leading-tight text-[color:var(--text-color,#111827)] sm:text-5xl">
                Turn finances into a game and unlock real-world wealth.
              </h1>
              <p className="text-lg text-[color:var(--muted-text,#6b7280)] sm:text-xl">
                Learn money skills in 5-minute missions, collect rewards, and get personalized guidance from an AI tutor that never sleeps.
              </p>

              <div className="grid gap-3 sm:grid-cols-3">
                {highlights.map((item) => (
                  <div
                    key={item.title}
                    className="flex items-start gap-3 rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-white/70 px-4 py-3 shadow-sm backdrop-blur"
                  >
                    <span className="mt-1 inline-flex h-8 w-8 items-center justify-center rounded-full bg-[color:var(--primary,#1d5330)]/10 text-[color:var(--primary,#1d5330)]">
                      {item.icon}
                    </span>
                    <div>
                      <p className="text-sm font-semibold text-[color:var(--text-color,#111827)]">{item.title}</p>
                      <p className="text-xs text-[color:var(--muted-text,#6b7280)]">{item.description}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <GlassButton
                  type="button"
                  onClick={() => navigate("/register")}
                  variant="primary"
                  className="w-full sm:w-auto"
                >
                  Start my financial journey
                </GlassButton>
                <GlassButton
                  type="button"
                  onClick={() => navigate("/login")}
                  variant="ghost"
                  className="w-full sm:w-auto"
                >
                  I already have an account
                </GlassButton>
              </div>

              <div className="flex flex-wrap gap-6 text-sm text-[color:var(--muted-text,#6b7280)]">
                <span className="inline-flex items-center gap-2 rounded-full bg-white/70 px-3 py-2 shadow-sm">
                  <Award className="h-4 w-4 text-[color:var(--primary,#1d5330)]" />
                  Budget Boss badge ready for you
                </span>
                <span className="inline-flex items-center gap-2 rounded-full bg-white/70 px-3 py-2 shadow-sm">
                  <BarChartLine className="h-4 w-4 text-[color:var(--primary,#1d5330)]" />
                  Track goals with XP and streaks
                </span>
                <span className="inline-flex items-center gap-2 rounded-full bg-white/70 px-3 py-2 shadow-sm">
                  <ChatDots className="h-4 w-4 text-[color:var(--primary,#1d5330)]" />
                  Ask our AI tutor anything, anytime
                </span>
              </div>
            </div>

            <div className="relative flex items-center justify-center">
              <div className="absolute -left-6 top-6 h-24 w-24 rounded-full bg-emerald-200/50 blur-2xl" aria-hidden />
              <div className="absolute -right-8 bottom-10 h-28 w-28 rounded-full bg-sky-200/60 blur-2xl" aria-hidden />
              <GlassCard className="relative w-full max-w-xl border border-[color:var(--border-color,#d1d5db)] bg-white/80 p-4 shadow-xl">
                <div className="flex items-center justify-between rounded-2xl bg-[color:var(--input-bg,#f3f4f6)] px-4 py-3 text-xs font-semibold uppercase tracking-wide text-[color:var(--muted-text,#6b7280)]">
                  <span>Finance quest preview</span>
                  <span className="inline-flex items-center gap-1 rounded-full bg-emerald-100/80 px-3 py-1 text-[color:var(--primary,#1d5330)]">+20 XP</span>
                </div>
                <div className="grid gap-4 pt-4 sm:grid-cols-2">
                  <div className="space-y-3 rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-white/90 p-4 shadow-sm">
                    <p className="text-xs font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">Streak mission</p>
                    <p className="text-lg font-semibold text-[color:var(--text-color,#111827)]">Complete your first quiz</p>
                    <p className="text-sm text-[color:var(--muted-text,#6b7280)]">Earn the “Budget Boss” badge when you finish.</p>
                    <div className="flex items-center gap-3">
                      <div className="h-2.5 w-full rounded-full bg-slate-100">
                        <div className="h-full w-2/3 rounded-full bg-gradient-to-r from-emerald-500 to-emerald-400" />
                      </div>
                      <span className="text-xs font-semibold text-[color:var(--text-color,#111827)]">66%</span>
                    </div>
                  </div>
                  <div className="space-y-3 rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-white/90 p-4 shadow-sm">
                    <p className="text-xs font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">Live tools</p>
                    <p className="text-lg font-semibold text-[color:var(--text-color,#111827)]">Budget in action</p>
                    <p className="text-sm text-[color:var(--muted-text,#6b7280)]">Adjust sliders to see how savings and investments grow.</p>
                    <div className="flex items-center justify-between rounded-xl bg-[color:var(--input-bg,#f3f4f6)] px-3 py-2 text-sm">
                      <span className="font-semibold text-[color:var(--text-color,#111827)]">Savings boost</span>
                      <span className="rounded-full bg-white px-3 py-1 text-[color:var(--primary,#1d5330)]">+15%</span>
                    </div>
                  </div>
                </div>
              </GlassCard>
            </div>
          </section>

          <section className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {valueProps.map((item) => (
              <GlassCard
                key={item.title}
                className="relative h-full overflow-hidden border border-[color:var(--border-color,#d1d5db)] bg-white/80 p-6 shadow-lg"
              >
                <span className="inline-flex items-center rounded-full bg-[color:var(--primary,#1d5330)]/10 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">
                  {item.badge}
                </span>
                <h3 className="mt-4 text-xl font-semibold text-[color:var(--text-color,#111827)]">{item.title}</h3>
                <p className="mt-2 text-sm text-[color:var(--muted-text,#6b7280)]">{item.text}</p>
                <div className="absolute -right-6 -top-6 h-20 w-20 rounded-full bg-[color:var(--primary,#1d5330)]/5" aria-hidden />
                <div className="absolute -left-4 bottom-0 h-16 w-16 rounded-full bg-sky-200/30" aria-hidden />
              </GlassCard>
            ))}
          </section>

          {featureSections.map((feature, index) => (
            <GlassCard key={feature.title} padding="lg" className="relative overflow-hidden p-6 lg:p-12">
              <div className="absolute inset-0 -z-10 bg-gradient-to-br from-white via-white to-emerald-50" aria-hidden />
              <div
                className={`flex flex-col gap-10 lg:flex-row ${
                  index % 2 !== 0 ? "lg:flex-row-reverse" : ""
                }`}
              >
                <div className="flex w-full flex-col justify-center gap-6 lg:w-1/2">
                  <div className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-[color:var(--primary,#1d5330)]/10">
                    {feature.icon}
                  </div>
                  <h2 className="text-3xl font-bold text-[color:var(--text-color,#111827)] lg:text-4xl">
                    {feature.title}
                  </h2>
                  <p className="text-base text-[color:var(--muted-text,#6b7280)] lg:text-lg">
                    {feature.text}
                  </p>
                  <ul className="space-y-2 text-sm text-[color:var(--text-color,#111827)]">
                    {feature.bullets.map((bullet) => (
                      <li key={bullet} className="flex items-start gap-2">
                        <span className="mt-0.5 text-[color:var(--primary,#1d5330)]">✓</span>
                        <span>{bullet}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="w-full lg:w-1/2">
                  <div className="relative overflow-hidden rounded-3xl border border-[color:var(--border-color,#d1d5db)] bg-[color:var(--input-bg,#f3f4f6)] p-4 shadow-lg shadow-[color:var(--shadow-color,rgba(0,0,0,0.1))]">
                    <div className="absolute -right-10 top-10 h-32 w-32 rounded-full bg-[color:var(--primary,#1d5330)]/10 blur-3xl" />
                    <img
                      src={feature.mockup}
                      alt={feature.title}
                      className="relative z-[1] w-full rounded-2xl object-cover"
                      loading="lazy"
                    />
                  </div>
                </div>
              </div>
            </GlassCard>
          ))}

          <section className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr]">
            <GlassCard padding="lg" className="relative overflow-hidden p-8">
              <div className="absolute inset-0 -z-10 bg-gradient-to-br from-emerald-50 via-white to-sky-50" aria-hidden />
              <div className="space-y-3">
                <div className="inline-flex items-center rounded-full bg-[color:var(--primary,#1d5330)]/10 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">
                  AI tutor & finance tools
                </div>
                <h3 className="text-3xl font-bold text-[color:var(--text-color,#111827)]">Ask, calculate, and act without leaving the page.</h3>
                <p className="text-base text-[color:var(--muted-text,#6b7280)]">
                  The Monevo AI assistant is always on, explaining concepts, running numbers, and crafting step-by-step plans while you learn.
                </p>
              </div>

              <div className="mt-8 grid gap-4 sm:grid-cols-2">
                {["Chat walkthroughs with real-time clarifications", "Budget, ROI, and payoff calculators built-in", "Instant rewrites if something is confusing", "Track your streaks and XP while you practice"].map((item) => (
                  <div
                    key={item}
                    className="flex items-start gap-3 rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-white/80 px-4 py-3 shadow-sm"
                  >
                    <span className="mt-1 inline-flex h-8 w-8 items-center justify-center rounded-full bg-[color:var(--primary,#1d5330)]/10 text-[color:var(--primary,#1d5330)]">
                      ✓
                    </span>
                    <p className="text-sm text-[color:var(--text-color,#111827)]">{item}</p>
                  </div>
                ))}
              </div>
            </GlassCard>

            <GlassCard className="relative overflow-hidden border border-[color:var(--border-color,#d1d5db)] bg-white/85 p-6 shadow-xl">
              <div className="absolute -right-10 top-0 h-48 w-48 rounded-full bg-[color:var(--primary,#1d5330)]/10 blur-3xl" aria-hidden />
              <div className="space-y-4">
                <div className="flex items-center gap-3 rounded-2xl bg-[color:var(--input-bg,#f3f4f6)] px-4 py-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500/10 text-emerald-600">
                    <ChatDots />
                  </div>
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">AI chat in action</p>
                    <p className="text-sm text-[color:var(--text-color,#111827)]">How do I build a 3-month emergency fund?</p>
                  </div>
                </div>
                <div className="space-y-3 rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-white/90 p-4 shadow-inner">
                  <p className="text-xs font-semibold uppercase tracking-wide text-[color:var(--muted-text,#6b7280)]">Assistant reply</p>
                  <p className="text-sm leading-relaxed text-[color:var(--text-color,#111827)]">
                    Split a target of $4,500 into 6 bi-weekly deposits: $375 each. Route them to a high-yield savings account. I’ll set reminders and track your streak so you don’t miss a contribution.
                  </p>
                  <div className="flex flex-wrap gap-2 text-xs font-semibold">
                    <span className="rounded-full bg-emerald-100/80 px-3 py-1 text-[color:var(--primary,#1d5330)]">Create plan</span>
                    <span className="rounded-full bg-sky-100/80 px-3 py-1 text-sky-700">Run calculator</span>
                    <span className="rounded-full bg-amber-100/80 px-3 py-1 text-amber-700">Save note</span>
                  </div>
                </div>
              </div>
            </GlassCard>
          </section>

          <section className="grid gap-6 lg:grid-cols-[1fr_1fr]">
            <GlassCard className="relative overflow-hidden border border-[color:var(--border-color,#d1d5db)] bg-white/80 p-8 shadow-xl">
              <div className="absolute -left-10 top-0 h-32 w-32 rounded-full bg-sky-200/30 blur-3xl" aria-hidden />
              <div className="absolute right-4 top-4 inline-flex items-center gap-2 rounded-full bg-emerald-100/70 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">
                Interactive & gamified
              </div>
              <h3 className="text-3xl font-bold text-[color:var(--text-color,#111827)]">Learning that clicks, taps, and rewards.</h3>
              <p className="mt-3 text-base text-[color:var(--muted-text,#6b7280)]">
                Try a quick product tour: quizzes trigger badges, streak counters reward daily practice, and mini tools let you see the impact of choices instantly.
              </p>
              <div className="mt-6 grid gap-4 sm:grid-cols-2">
                {["Animated product tours", "Interactive calculators", "Level-up quests", "Leaderboard highlights"].map((item) => (
                  <div key={item} className="flex items-center gap-3 rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-white/80 px-3 py-2">
                    <span className="text-[color:var(--primary,#1d5330)]">★</span>
                    <p className="text-sm text-[color:var(--text-color,#111827)]">{item}</p>
                  </div>
                ))}
              </div>
            </GlassCard>

            <GlassCard className="relative overflow-hidden border border-[color:var(--border-color,#d1d5db)] bg-white/85 p-8 shadow-xl">
              <div className="absolute -right-8 top-0 h-32 w-32 rounded-full bg-emerald-200/40 blur-3xl" aria-hidden />
              <h3 className="text-3xl font-bold text-[color:var(--text-color,#111827)]">Micro-lessons with rich content.</h3>
              <p className="mt-3 text-base text-[color:var(--muted-text,#6b7280)]">
                Over 100 lessons combining media, practice, and feedback so you learn fast and retain more.
              </p>
              <div className="mt-6 grid gap-3">
                {lessonTypes.map((item) => (
                  <div key={item.title} className="flex items-center justify-between rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-white/80 px-4 py-3 text-sm">
                    <div>
                      <p className="font-semibold text-[color:var(--text-color,#111827)]">{item.title}</p>
                      <p className="text-[color:var(--muted-text,#6b7280)]">{item.detail}</p>
                    </div>
                    <span className="rounded-full bg-[color:var(--primary,#1d5330)]/10 px-3 py-1 text-xs font-semibold text-[color:var(--primary,#1d5330)]">Quick</span>
                  </div>
                ))}
              </div>
            </GlassCard>
          </section>

          <GlassCard padding="lg" className="relative overflow-hidden p-8">
            <div className="absolute inset-0 -z-10 bg-gradient-to-r from-emerald-50 via-white to-sky-50" aria-hidden />
            <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
              <div className="space-y-3">
                <div className="inline-flex items-center rounded-full bg-[color:var(--primary,#1d5330)]/10 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">
                  Social proof
                </div>
                <h3 className="text-3xl font-bold text-[color:var(--text-color,#111827)]">Learners stay because progress feels rewarding.</h3>
                <p className="text-base text-[color:var(--muted-text,#6b7280)]">
                  See what the community is achieving with streaks, badges, and real financial wins.
                </p>
                <div className="grid gap-4 sm:grid-cols-2">
                  {stats.map((stat) => (
                    <div key={stat.label} className="flex flex-col rounded-2xl border border-[color:var(--border-color,#d1d5db)] bg-white/80 px-4 py-3 shadow-sm">
                      <span className="text-2xl font-bold text-[color:var(--text-color,#111827)]">{stat.value}</span>
                      <span className="text-sm text-[color:var(--muted-text,#6b7280)]">{stat.label}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex w-full max-w-md flex-col gap-4 rounded-3xl border border-[color:var(--border-color,#d1d5db)] bg-white/90 p-6 shadow-inner">
                <p className="text-sm font-semibold uppercase tracking-wide text-[color:var(--primary,#1d5330)]">What learners say</p>
                <blockquote className="text-base leading-relaxed text-[color:var(--text-color,#111827)]">
                  “I finally understand budgeting. The streaks keep me accountable and the AI tutor explains things without jargon.”
                </blockquote>
                <p className="text-sm font-semibold text-[color:var(--text-color,#111827)]">Ariel, unlocked the Budget Boss badge in 6 days</p>
              </div>
            </div>
          </GlassCard>

          <GlassCard padding="lg" className="relative overflow-hidden p-10 text-center">
            <div className="absolute inset-0 -z-10 bg-gradient-to-b from-emerald-50 via-white to-sky-50" aria-hidden />
            <h3 className="text-3xl font-bold text-[color:var(--text-color,#111827)] sm:text-4xl">
              Stop stressing about money. Start mastering it today.
            </h3>
            <p className="mt-3 text-sm text-[color:var(--muted-text,#6b7280)] sm:text-base">
              Create a free account to unlock your first lesson, earn your first badge, and see your progress bar fill up.
            </p>
            <div className="mt-6 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <GlassButton
                type="button"
                onClick={() => navigate("/register")}
                variant="primary"
              >
                Create my free account
              </GlassButton>
              <GlassButton
                type="button"
                onClick={() => navigate("/login")}
                variant="ghost"
              >
                Already a member? Log in
              </GlassButton>
            </div>
          </GlassCard>
        </div>
      </main>
    </div>
  );
}

export default Welcome;
