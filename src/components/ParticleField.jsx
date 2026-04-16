import { useEffect, useRef } from "react";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";

// Each orb: position (%), size (px), opacity, animation duration & delay
const ORBS = [
  { x: 15, y: 25, size: 520, opacity: 0.13, duration: 18, delay: 0,   depth: 0.04 },
  { x: 72, y: 18, size: 380, opacity: 0.10, duration: 22, delay: 3,   depth: 0.07 },
  { x: 55, y: 65, size: 460, opacity: 0.09, duration: 26, delay: 6,   depth: 0.03 },
  { x: 88, y: 55, size: 300, opacity: 0.11, duration: 20, delay: 9,   depth: 0.06 },
  { x: 30, y: 75, size: 340, opacity: 0.08, duration: 24, delay: 12,  depth: 0.05 },
];

const Orb = ({ orb, mouseX, mouseY }) => {
  // Parallax: each orb moves at a different depth fraction of the mouse offset
  const x = useTransform(mouseX, (v) => v * orb.depth);
  const y = useTransform(mouseY, (v) => v * orb.depth);

  return (
    <motion.div
      className="pointer-events-none absolute rounded-full"
      style={{
        left: `${orb.x}%`,
        top: `${orb.y}%`,
        width: orb.size,
        height: orb.size,
        translateX: x,
        translateY: y,
        // Amber/gold tint matching the site accent — adjust hue to taste
        background:
          "radial-gradient(circle, oklch(0.82 0.14 80 / 1) 0%, transparent 70%)",
        filter: "blur(72px)",
        opacity: orb.opacity,
        // offset by half size so the orb is centered on its x/y
        marginLeft: -orb.size / 2,
        marginTop: -orb.size / 2,
      }}
      animate={{
        // Gentle float: drifts up/down and slightly scales
        y: ["-2%", "2%", "-2%"],
        scale: [1, 1.06, 1],
      }}
      transition={{
        duration: orb.duration,
        delay: orb.delay,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    />
  );
};

const ParticleField = () => {
  const ref = useRef(null);

  // Raw mouse values — large range so parallax is readable
  const rawX = useMotionValue(0);
  const rawY = useMotionValue(0);

  // Spring smoothing so the orbs lag behind the cursor naturally
  const mouseX = useSpring(rawX, { stiffness: 40, damping: 25 });
  const mouseY = useSpring(rawY, { stiffness: 40, damping: 25 });

  useEffect(() => {
    const handleMove = (e) => {
      const rect = ref.current?.getBoundingClientRect();
      if (!rect) return;
      // Map mouse position to -200/+200 range
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      rawX.set((e.clientX - cx) * 0.4);
      rawY.set((e.clientY - cy) * 0.4);
    };

    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, [rawX, rawY]);

  return (
    <div
      ref={ref}
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 overflow-hidden"
    >
      {/* Dot grid — subtle texture anchoring the floating orbs */}
      <div
        className="absolute inset-0 opacity-[0.035] dark:opacity-[0.055]"
        style={{
          backgroundImage:
            "radial-gradient(circle, currentColor 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }}
      />

      {/* Floating orbs */}
      {ORBS.map((orb, i) => (
        <Orb key={i} orb={orb} mouseX={mouseX} mouseY={mouseY} />
      ))}

      {/* Vignette: darkens edges so orbs don't bleed into other sections */}
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse 80% 70% at 50% 50%, transparent 40%, var(--color-bg, #0d0d0d) 100%)",
        }}
      />
    </div>
  );
};

export default ParticleField;
