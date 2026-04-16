import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Services from "../components/Services";
import Projects from "../components/Projects";
import Process from "../components/Process";
import About from "../components/About";
import Contact from "../components/Contact";
import Footer from "../components/Footer";
import ParallaxBubbles from "../components/ui/ParallaxBubbles";

const Home = () => {
  return (
    <div className="relative min-h-screen text-ink-900 dark:text-paper-50 transition-colors duration-300">
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 z-0 bg-paper-50 dark:bg-ink-950"
      />
      <ParallaxBubbles />
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 z-[2] opacity-[0.1] grain-bg dark:opacity-[0.14]"
      />
      <div className="relative z-10">
        <Navbar />
        <main>
          <Hero />
          <Services />
          <Projects />
          <Process />
          <About />
          <Contact />
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default Home;
