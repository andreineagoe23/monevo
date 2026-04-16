import { motion } from "framer-motion";
import Section from "./ui/Section";

const About = () => {
  return (
    <Section id="about" eyebrow="About">
      <div className="grid grid-cols-1 gap-12 md:grid-cols-12 md:gap-16">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="md:col-span-6"
        >
          <p className="font-display text-3xl leading-[1.1] tracking-tightest text-ink-900 dark:text-paper-50 sm:text-4xl md:text-5xl">
            &ldquo;The site itself should be the proof
            <span className="italic text-amber-500 dark:text-amber-400">
              {" "}
              of the work.
            </span>
            &rdquo;
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="space-y-5 text-base leading-relaxed text-muted-light dark:text-muted-dark md:col-span-6 md:text-lg"
        >
          <p>
            I&rsquo;m Andrei. I spent years at Framestore shipping polished
            interactive work for some of the biggest brands in the world &mdash;
            now I build the same caliber of site for local businesses that
            actually need them.
          </p>
          <p>
            Every project is hands-on, from first sketch to launch day. No
            account managers, no offshore handoffs, no templated deliverables.
            One craftsman, one client, one clean build.
          </p>
          <p>
            If you care about the details, we&rsquo;ll get on.
          </p>
        </motion.div>
      </div>
    </Section>
  );
};

export default About;
