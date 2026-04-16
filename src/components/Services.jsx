import { motion } from "framer-motion";
import Section from "./ui/Section";
import SectionHeading from "./ui/SectionHeading";

const services = [
  {
    ordinal: "01",
    title: "Web design",
    body:
      "Layouts that feel considered, not templated. Typography, rhythm, and details that make a brand feel premium the second a visitor lands.",
    bullets: ["Visual identity", "Art direction", "Design systems"],
  },
  {
    ordinal: "02",
    title: "Custom development",
    body:
      "Hand-built React, Next.js and headless stacks. Fast, accessible, maintainable — no page-builder bloat, no templates you have to fight.",
    bullets: ["React / Next.js", "Headless CMS", "CI / CD"],
  },
  {
    ordinal: "03",
    title: "SEO-ready builds",
    body:
      "Clean semantic HTML, sub-second performance, structured data and metadata done right — so Google and your customers actually find you.",
    bullets: ["Core Web Vitals", "Semantic HTML", "Schema & metadata"],
  },
];

const ServiceCard = ({ ordinal, title, body, bullets, offsetClassName }) => (
  <motion.div
    initial={{ opacity: 0, y: 24 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-80px" }}
    transition={{ duration: 0.6 }}
    className={`relative flex flex-col gap-6 rounded-2xl border border-ink-900/10 bg-paper-100 p-8 md:p-10 dark:border-paper-50/10 dark:bg-ink-900 ${offsetClassName ?? ""}`}
  >
    <span className="font-display text-3xl text-amber-500 dark:text-amber-400">
      {ordinal}
    </span>
    <h3 className="font-display text-3xl tracking-tightest text-ink-900 dark:text-paper-50 md:text-4xl">
      {title}
    </h3>
    <p className="max-w-md text-base leading-relaxed text-muted-light dark:text-muted-dark">
      {body}
    </p>
    <ul className="mt-auto flex flex-wrap gap-x-6 gap-y-2 pt-4 text-sm text-ink-900/70 dark:text-paper-50/70">
      {bullets.map((b) => (
        <li key={b} className="flex items-center gap-2">
          <span className="h-1 w-1 rounded-full bg-amber-500" />
          {b}
        </li>
      ))}
    </ul>
  </motion.div>
);

const Services = () => {
  return (
    <Section id="services" eyebrow="Services">
      <SectionHeading
        subtitle="Three things I do, and I do them properly. No bloated packages, no filler — every engagement is scoped around what actually moves the needle for your business."
      >
        Craft, not a <span className="italic text-amber-500 dark:text-amber-400">package</span>.
      </SectionHeading>

      <div className="mt-16 grid grid-cols-1 gap-6 md:grid-cols-12 md:gap-8">
        <div className="md:col-span-7">
          <ServiceCard {...services[0]} />
        </div>
        <div className="md:col-span-5 md:mt-16">
          <ServiceCard {...services[1]} />
        </div>
        <div className="md:col-span-8 md:col-start-3 md:mt-6">
          <ServiceCard {...services[2]} />
        </div>
      </div>
    </Section>
  );
};

export default Services;
