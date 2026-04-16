const Badge = ({ children, className = "" }) => {
  return (
    <span
      className={`inline-flex items-center rounded-full border border-amber-500/30 px-3 py-1 text-[0.7rem] font-medium uppercase tracking-wider text-amber-500 dark:text-amber-400 ${className}`}
    >
      {children}
    </span>
  );
};

export default Badge;
