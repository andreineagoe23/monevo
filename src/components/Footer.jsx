import { motion } from "framer-motion";
import { Github, Linkedin, Mail } from "lucide-react";

const socials = [
  {
    name: "GitHub",
    icon: Github,
    href: "https://github.com/andreineagoe23",
  },
  {
    name: "LinkedIn",
    icon: Linkedin,
    href: "https://linkedin.com/in/andrei-neagoe-29a937256",
  },
  {
    name: "Email",
    icon: Mail,
    href: "mailto:neagoeandrei23@gmail.com",
  },
];

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-ink-900/10 bg-transparent dark:border-paper-50/10">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-6 py-10 sm:flex-row sm:items-center sm:justify-between sm:px-8 lg:px-12">
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="flex flex-col"
        >
          <span className="font-display text-2xl tracking-tightest text-ink-900 dark:text-paper-50">
            Monevo
          </span>
          <a
            href="https://www.monevo.tech"
            className="text-xs uppercase tracking-[0.2em] text-muted-light transition-colors duration-200 hover:text-amber-500 dark:text-muted-dark dark:hover:text-amber-400"
          >
            monevo.tech
          </a>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.05 }}
          className="flex items-center gap-3"
        >
          {socials.map((s) => (
            <a
              key={s.name}
              href={s.href}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={s.name}
              className="rounded-full border border-ink-900/10 p-2.5 text-ink-900/70 transition-all duration-200 hover:border-amber-500 hover:text-amber-500 dark:border-paper-50/10 dark:text-paper-50/70 dark:hover:border-amber-400 dark:hover:text-amber-400"
            >
              <s.icon className="h-4 w-4" />
            </a>
          ))}
        </motion.div>
      </div>

      <div className="border-t border-ink-900/5 dark:border-paper-50/5">
        <div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-2 px-6 py-5 text-xs text-muted-light sm:flex-row sm:items-center sm:px-8 dark:text-muted-dark lg:px-12">
          <span>&copy; {year} Monevo &middot; Built by Andrei Neagoe</span>
          <span className="uppercase tracking-[0.2em]">Chigwell &mdash; London</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
