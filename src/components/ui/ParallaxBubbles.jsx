import { motion, useScroll, useTransform, useReducedMotion } from "framer-motion";

/** Fixed viewport layer — positions are % of viewport; scroll is tied to the full document for one continuous field (common “blob hero” pattern). */
const DEFAULT_BUBBLES = [
  { top: "-8%", left: "-12%", size: 680, speed: -0.42, opacity: 0.42, delay: 0, duration: 16 },
  { top: "12%", left: "68%", size: 560, speed: -0.58, opacity: 0.36, delay: 1.4, duration: 18 },
  { top: "38%", left: "-6%", size: 620, speed: -0.48, opacity: 0.38, delay: 2.2, duration: 20 },
  { top: "52%", left: "48%", size: 720, speed: -0.32, opacity: 0.28, delay: 0.8, duration: 22 },
  { top: "78%", left: "8%", size: 540, speed: -0.52, opacity: 0.34, delay: 2.8, duration: 14 },
  { top: "92%", left: "72%", size: 480, speed: -0.38, opacity: 0.32, delay: 1.1, duration: 17 },
  { top: "22%", left: "28%", size: 900, speed: -0.22, opacity: 0.18, delay: 3.2, duration: 24 },
];

const ParallaxBubbles = ({ bubbles = DEFAULT_BUBBLES, className = "" }) => {
  const prefersReducedMotion = useReducedMotion();
  const { scrollYProgress } = useScroll();

  return (
    <div
      aria-hidden
      className={`pointer-events-none fixed inset-0 z-[1] overflow-hidden ${className}`}
    >
      {bubbles.map((b, i) => (
        <Bubble
          key={i}
          bubble={b}
          scrollYProgress={scrollYProgress}
          reduced={!!prefersReducedMotion}
        />
      ))}
    </div>
  );
};

const Bubble = ({ bubble, scrollYProgress, reduced }) => {
  const travel = reduced ? 0 : bubble.speed * 380;
  const y = useTransform(scrollYProgress, [0, 1], [0, travel]);

  return (
    <motion.div
      style={{
        top: bubble.top,
        left: bubble.left,
        width: bubble.size,
        height: bubble.size,
        opacity: bubble.opacity,
        y,
      }}
      animate={
        reduced
          ? undefined
          : {
              scale: [1, 1.06, 0.98, 1],
              x: [0, 18, -12, 0],
            }
      }
      transition={
        reduced
          ? undefined
          : {
              duration: bubble.duration,
              repeat: Infinity,
              ease: "easeInOut",
              delay: bubble.delay,
            }
      }
      className="absolute rounded-full bg-[radial-gradient(circle_at_center,_rgba(242,201,122,0.85),_rgba(217,154,62,0.32)_42%,_transparent_70%)] blur-3xl"
    />
  );
};

export default ParallaxBubbles;
