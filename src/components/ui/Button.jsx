import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

const baseClasses =
  "inline-flex items-center justify-center gap-2 font-medium transition-colors duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400 focus-visible:ring-offset-2 focus-visible:ring-offset-ink-950 dark:focus-visible:ring-offset-ink-950";

const variants = {
  primary:
    "px-6 py-3 rounded-full bg-amber-400 text-ink-950 hover:bg-amber-300 shadow-[0_0_0_1px_rgba(231,179,90,0.3)]",
  ghost:
    "px-6 py-3 rounded-full border border-ink-900/20 dark:border-paper-50/20 text-ink-900 dark:text-paper-50 hover:border-amber-400 hover:text-amber-400",
  link: "text-sm text-amber-400 hover:text-amber-300 group",
};

const Button = ({
  as: Tag = "button",
  variant = "primary",
  className = "",
  children,
  showArrow = false,
  ...props
}) => {
  const classes = `${baseClasses} ${variants[variant] ?? variants.primary} ${className}`;

  if (Tag === "a") {
    return (
      <motion.a
        whileHover={{ y: variant === "link" ? 0 : -2 }}
        whileTap={{ scale: 0.97 }}
        className={classes}
        {...props}
      >
        {children}
        {showArrow && (
          <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
        )}
      </motion.a>
    );
  }

  return (
    <motion.button
      whileHover={{ y: variant === "link" ? 0 : -2 }}
      whileTap={{ scale: 0.97 }}
      className={classes}
      {...props}
    >
      {children}
      {showArrow && (
        <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
      )}
    </motion.button>
  );
};

export default Button;
