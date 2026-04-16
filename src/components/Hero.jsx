import { motion } from "framer-motion";
import Button from "./ui/Button";

const HEADLINE = [
  "Web",
  "design",
  "and",
  "builds",
  "for",
  "the",
  "long",
  "game.",
];

const scrollTo = (id) => {
  const el = document.querySelector(id);
  if (el) el.scrollIntoView({ behavior: "smooth" });
};

const wordVariants = {
  hidden: { y: 32, opacity: 0 },
  show: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.7, ease: [0.2, 0.8, 0.2, 1] },
  },
};

const Hero = () => {
  return (
    <section
      id="hero"
      className="relative flex min-h-screen items-center overflow-hidden bg-transparent pt-28 pb-16 md:pt-0 md:pb-0"
    >
      <div className="relative mx-auto w-full max-w-7xl px-6 sm:px-8 lg:px-12">
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-10 flex items-center gap-3 text-xs uppercase tracking-[0.28em] text-amber-500 dark:text-amber-400"
        >
          <span className="h-px w-10 bg-amber-500/60" />
          <span>Andrei Neagoe &mdash; Monevo</span>
        </motion.div>

        <motion.h1
          initial="hidden"
          animate="show"
          transition={{ staggerChildren: 0.08, delayChildren: 0.1 }}
          className="font-display text-[clamp(2.75rem,9vw,7.5rem)] leading-[0.95] tracking-tightest text-ink-900 dark:text-paper-50 [overflow-wrap:break-word]"
        >
          {HEADLINE.map((word, i) => (
            <motion.span
              key={`${word}-${i}`}
              variants={wordVariants}
              className="mr-[0.25em] inline-block"
            >
              {word === "long" ? (
                <span className="italic text-amber-500 dark:text-amber-400">
                  {word}
                </span>
              ) : (
                word
              )}
            </motion.span>
          ))}
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9, duration: 0.6 }}
          className="mt-10 max-w-xl text-base leading-relaxed text-muted-light dark:text-muted-dark md:text-lg"
        >
          Handcrafted web design and custom development for local businesses
          that actually need to convert. One client at a time, end to end.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.1, duration: 0.6 }}
          className="mt-12 flex flex-col gap-4 sm:flex-row sm:items-center"
        >
          <Button
            variant="primary"
            onClick={() => scrollTo("#work")}
            showArrow
          >
            See work
          </Button>
          <Button variant="ghost" onClick={() => scrollTo("#contact")}>
            Let&rsquo;s talk
          </Button>
        </motion.div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 amber-hairline" />
    </section>
  );
};

export default Hero;
