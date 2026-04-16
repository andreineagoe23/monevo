import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Moon, Sun, Menu, X } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

const navItems = [
  { name: "Work", href: "#work" },
  { name: "Services", href: "#services" },
  { name: "Process", href: "#process" },
  { name: "About", href: "#about" },
  { name: "Contact", href: "#contact" },
];

const Logo = () => (
  <div className="flex items-center gap-2">
    <svg viewBox="0 0 64 64" className="h-7 w-7 flex-shrink-0" aria-hidden>
      <rect width="64" height="64" rx="12" className="fill-ink-900 dark:fill-ink-800" />
      <path
        d="M14 48 V18 L32 38 L50 18 V48"
        fill="none"
        stroke="currentColor"
        strokeWidth="5"
        strokeLinecap="square"
        strokeLinejoin="miter"
        className="text-amber-400"
      />
    </svg>
    <span className="font-display text-xl tracking-tightest sm:text-2xl">Monevo</span>
  </div>
);

const Navbar = () => {
  const { darkMode, toggleDarkMode } = useTheme();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 32);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const goTo = (href) => {
    const el = document.querySelector(href);
    if (el) el.scrollIntoView({ behavior: "smooth" });
    setOpen(false);
  };

  return (
    <motion.nav
      initial={{ y: -60, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className={`fixed inset-x-0 top-0 z-50 transition-colors duration-300 ${
        scrolled
          ? "border-b border-amber-500/20 bg-paper-50/80 backdrop-blur-md dark:bg-ink-950/80"
          : "bg-transparent"
      }`}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 sm:px-8 lg:px-12">
        <button
          onClick={() => goTo("#hero")}
          className="flex items-center gap-2 text-ink-900 transition-colors duration-200 hover:text-amber-500 dark:text-paper-50 dark:hover:text-amber-400"
          aria-label="Monevo home"
        >
          <Logo />
        </button>

        <div className="hidden items-center gap-8 md:flex">
          {navItems.map((item) => (
            <button
              key={item.name}
              onClick={() => goTo(item.href)}
              className="text-sm text-ink-900/80 transition-colors duration-200 hover:text-amber-500 dark:text-paper-50/80 dark:hover:text-amber-400"
            >
              {item.name}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={toggleDarkMode}
            className="rounded-full p-2 text-ink-900/70 transition-colors duration-200 hover:bg-ink-900/5 hover:text-amber-500 dark:text-paper-50/70 dark:hover:bg-paper-50/5 dark:hover:text-amber-400"
            aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>

          <button
            onClick={() => setOpen((v) => !v)}
            className="rounded-full p-2 text-ink-900/70 transition-colors duration-200 hover:bg-ink-900/5 hover:text-amber-500 md:hidden dark:text-paper-50/70 dark:hover:bg-paper-50/5 dark:hover:text-amber-400"
            aria-label="Toggle menu"
            aria-expanded={open}
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden border-t border-amber-500/20 bg-paper-50/95 backdrop-blur-md md:hidden dark:bg-ink-950/95"
          >
            <div className="flex flex-col px-6 py-4">
              {navItems.map((item) => (
                <button
                  key={item.name}
                  onClick={() => goTo(item.href)}
                  className="py-3 text-left font-display text-2xl tracking-tightest text-ink-900 transition-colors duration-200 hover:text-amber-500 dark:text-paper-50 dark:hover:text-amber-400"
                >
                  {item.name}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

export default Navbar;
