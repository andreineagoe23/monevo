import { motion } from "framer-motion";

const Section = ({
  id,
  eyebrow,
  className = "",
  containerClassName = "",
  children,
  ...props
}) => {
  return (
    <section
      id={id}
      className={`relative py-24 md:py-32 ${className}`}
      {...props}
    >
      <div
        className={`mx-auto w-full max-w-7xl px-6 sm:px-8 lg:px-12 ${containerClassName}`}
      >
        {eyebrow && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5 }}
            className="mb-6 flex items-center gap-3 text-xs uppercase tracking-[0.25em] text-amber-500 dark:text-amber-400"
          >
            <span className="h-px w-8 bg-amber-500/50" />
            <span>{eyebrow}</span>
          </motion.div>
        )}
        {children}
      </div>
    </section>
  );
};

export default Section;
