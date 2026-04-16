import { motion } from "framer-motion";

const toneClasses = {
  ink: "bg-ink-900 text-paper-50 border-paper-50/10",
  paper: "bg-paper-50 text-ink-900 border-ink-900/10",
  auto:
    "bg-paper-100 text-ink-900 border-ink-900/10 dark:bg-ink-900 dark:text-paper-50 dark:border-paper-50/10",
};

const Card = ({
  tone = "auto",
  className = "",
  children,
  hoverLift = true,
  ...props
}) => {
  return (
    <motion.div
      whileHover={hoverLift ? { y: -6 } : undefined}
      transition={{ type: "spring", stiffness: 260, damping: 22 }}
      className={`group relative rounded-2xl border p-8 transition-shadow duration-300 hover:shadow-[0_20px_50px_-20px_rgba(217,154,62,0.25)] ${toneClasses[tone]} ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export default Card;
