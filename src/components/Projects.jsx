import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import Section from "./ui/Section";
import SectionHeading from "./ui/SectionHeading";
import Badge from "./ui/Badge";
import { projects } from "../data/projects";

const spanClasses = {
  lg: "md:col-span-4",
  sm: "md:col-span-2",
};

const cleanUrl = (url) => url.replace(/^https?:\/\//, "").replace(/\/$/, "");

const ProjectCard = ({ project, index }) => {
  const ordinal = String(index + 1).padStart(2, "0");

  return (
    <motion.a
      href={project.url}
      target="_blank"
      rel="noopener noreferrer"
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.6, delay: index * 0.08 }}
      whileHover={{ y: -6 }}
      className={`group relative flex min-h-[280px] flex-col justify-between overflow-hidden rounded-2xl border border-ink-900/10 bg-paper-100 p-8 transition-shadow duration-300 hover:shadow-[0_30px_60px_-30px_rgba(217,154,62,0.35)] dark:border-paper-50/10 dark:bg-ink-900 md:min-h-[340px] md:p-10 ${spanClasses[project.span] ?? spanClasses.sm}`}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 rounded-full bg-amber-400/0 blur-3xl transition-all duration-500 group-hover:bg-amber-400/15"
      />

      <div className="flex items-start justify-between gap-4">
        <span className="font-display text-2xl text-amber-500 dark:text-amber-400">
          {ordinal}
        </span>
        <span className="max-w-[60%] truncate text-right text-xs uppercase tracking-[0.15em] text-muted-light dark:text-muted-dark">
          {cleanUrl(project.url)}
        </span>
      </div>

      <div className="mt-10 md:mt-14">
        <h3 className="font-display text-4xl leading-[0.95] tracking-tightest text-ink-900 transition-colors duration-300 group-hover:text-amber-500 dark:text-paper-50 dark:group-hover:text-amber-400 md:text-6xl">
          {project.name}
        </h3>
        <p className="mt-4 max-w-md text-base leading-relaxed text-muted-light dark:text-muted-dark">
          {project.pitch}
        </p>
      </div>

      <div className="mt-8 flex items-end justify-between gap-4">
        <div className="flex flex-wrap gap-2">
          {project.stack.map((tech) => (
            <Badge key={tech}>{tech}</Badge>
          ))}
        </div>
        <span className="inline-flex items-center gap-1 text-sm text-amber-500 opacity-0 transition-all duration-300 group-hover:translate-x-1 group-hover:opacity-100 dark:text-amber-400">
          Visit site
          <ArrowUpRight className="h-4 w-4" />
        </span>
      </div>
    </motion.a>
  );
};

const Projects = () => {
  return (
    <Section id="work" eyebrow="Selected work">
      <SectionHeading
        subtitle="Four projects, four contexts — from artisan software to a Romanian B2B brand. Every one is live, every one earned its keep."
      >
        The work speaks
        <br />
        <span className="italic text-amber-500 dark:text-amber-400">for itself.</span>
      </SectionHeading>

      <div className="mt-16 grid grid-cols-1 gap-6 md:grid-cols-6 md:gap-8">
        {projects.map((project, i) => (
          <ProjectCard key={project.id} project={project} index={i} />
        ))}
      </div>
    </Section>
  );
};

export default Projects;
