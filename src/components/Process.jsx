import { motion } from "framer-motion";
import Section from "./ui/Section";
import SectionHeading from "./ui/SectionHeading";

const steps = [
  {
    ordinal: "01",
    title: "Brief",
    description:
      "Quick call, clear goals. We lock scope, timeline, and what success actually looks like.",
  },
  {
    ordinal: "02",
    title: "Design",
    description:
      "Typography, layout, and art direction nailed down before a single line of code is written.",
  },
  {
    ordinal: "03",
    title: "Build",
    description:
      "Hand-coded in React. Accessible, performant, responsive — reviewed live at every milestone.",
  },
  {
    ordinal: "04",
    title: "Launch",
    description:
      "Deployed, tuned for speed and SEO, and handed over with everything you need to own it.",
  },
];

const Process = () => {
  return (
    <Section
      id="process"
      eyebrow="How we work"
      className="bg-paper-100/35 backdrop-blur-sm dark:bg-ink-900/30"
    >
      <SectionHeading
        subtitle="Four steps, no surprises. Same process whether it's a one-pager or a full custom build."
      >
        Brief. Design.
        <br />
        Build. <span className="italic text-amber-500 dark:text-amber-400">Launch.</span>
      </SectionHeading>

      <div className="mt-16 grid grid-cols-1 gap-10 sm:grid-cols-2 md:grid-cols-4 md:gap-6">
        {steps.map((step, i) => (
          <motion.div
            key={step.ordinal}
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6, delay: i * 0.08 }}
            className="relative flex flex-col gap-4"
          >
            {i < steps.length - 1 && (
              <div
                aria-hidden
                className="absolute left-12 right-0 top-7 hidden h-px bg-amber-500/30 md:block"
              />
            )}
            <span className="font-display text-5xl leading-none text-amber-500 dark:text-amber-400 md:text-6xl">
              {step.ordinal}
            </span>
            <h3 className="font-display text-2xl tracking-tightest text-ink-900 dark:text-paper-50">
              {step.title}
            </h3>
            <p className="max-w-xs text-sm leading-relaxed text-muted-light dark:text-muted-dark">
              {step.description}
            </p>
          </motion.div>
        ))}
      </div>
    </Section>
  );
};

export default Process;
