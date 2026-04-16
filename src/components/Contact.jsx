import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, MessageCircle, Send, CheckCircle, ArrowUpRight } from "lucide-react";
const EMAIL = "neagoeandrei23@gmail.com";
const WHATSAPP_NUMBER = "447543519824";

const Contact = () => {
  const [formData, setFormData] = useState({ name: "", email: "", message: "" });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const validate = () => {
    const e = {};
    if (!formData.name.trim()) e.name = "Name is required";
    if (!formData.email.trim()) e.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(formData.email)) e.email = "Email is invalid";
    if (!formData.message.trim()) e.message = "Message is required";
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((p) => ({ ...p, [name]: value }));
    if (errors[name]) setErrors((p) => ({ ...p, [name]: "" }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setIsSubmitting(true);
    // TODO: wire to Formspree or Resend endpoint. For now, fall through to mailto.
    await new Promise((r) => setTimeout(r, 900));
    setIsSubmitting(false);
    setIsSubmitted(true);
    setTimeout(() => {
      setIsSubmitted(false);
      setFormData({ name: "", email: "", message: "" });
    }, 3500);
  };

  return (
    <section
      id="contact"
      className="relative border-y border-paper-50/10 bg-ink-950/88 text-paper-50 backdrop-blur-xl dark:border-ink-900/10 dark:bg-paper-50/88 dark:text-ink-900"
    >
      <div className="pointer-events-none absolute inset-0 opacity-[0.06] grain-bg dark:opacity-[0.08]" />
      <div className="relative z-10 mx-auto w-full max-w-7xl px-6 py-24 sm:px-8 md:py-32 lg:px-12">
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.5 }}
          className="mb-6 flex items-center gap-3 text-xs uppercase tracking-[0.25em] text-amber-400 dark:text-amber-500"
        >
          <span className="h-px w-8 bg-amber-400/60 dark:bg-amber-500/60" />
          <span>Contact</span>
        </motion.div>

        <motion.h2
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl font-display text-[clamp(2.5rem,7vw,6rem)] leading-[0.95] tracking-tightest"
        >
          Let&rsquo;s talk about your{" "}
          <span className="italic text-amber-400 dark:text-amber-500">project.</span>
        </motion.h2>

        <motion.p
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mt-8 max-w-xl text-base leading-relaxed text-paper-50/70 dark:text-ink-900/70 md:text-lg"
        >
          Tell me what you&rsquo;re building. Quickest replies come via email or
          WhatsApp &mdash; or drop the details in the form below.
        </motion.p>

        <div className="mt-14 grid grid-cols-1 gap-10 lg:grid-cols-2 lg:gap-16">
          <div className="flex flex-col gap-4">
            <a
              href={`mailto:${EMAIL}`}
              className="group flex items-center justify-between gap-6 rounded-2xl border border-paper-50/15 p-6 transition-all duration-300 hover:border-amber-400 dark:border-ink-900/15 dark:hover:border-amber-500"
            >
              <div className="flex items-center gap-4">
                <Mail className="h-5 w-5 text-amber-400 dark:text-amber-500" />
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-paper-50/50 dark:text-ink-900/50">
                    Email
                  </p>
                  <p className="font-display text-xl">{EMAIL}</p>
                </div>
              </div>
              <ArrowUpRight className="h-5 w-5 transition-transform duration-300 group-hover:-translate-y-1 group-hover:translate-x-1" />
            </a>

            <a
              href={`https://wa.me/${WHATSAPP_NUMBER}`}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center justify-between gap-6 rounded-2xl border border-paper-50/15 p-6 transition-all duration-300 hover:border-amber-400 dark:border-ink-900/15 dark:hover:border-amber-500"
            >
              <div className="flex items-center gap-4">
                <MessageCircle className="h-5 w-5 text-amber-400 dark:text-amber-500" />
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-paper-50/50 dark:text-ink-900/50">
                    WhatsApp
                  </p>
                  <p className="font-display text-xl">+44 7543 519824</p>
                </div>
              </div>
              <ArrowUpRight className="h-5 w-5 transition-transform duration-300 group-hover:-translate-y-1 group-hover:translate-x-1" />
            </a>

            <div className="mt-4 text-xs uppercase tracking-[0.2em] text-paper-50/40 dark:text-ink-900/40">
              Based in Chigwell, Essex &mdash; working worldwide
            </div>
          </div>

          <motion.form
            onSubmit={handleSubmit}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6, delay: 0.15 }}
            className="relative"
          >
            {isSubmitted ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex flex-col items-start gap-4 rounded-2xl border border-amber-400/30 bg-amber-400/5 p-8"
              >
                <CheckCircle className="h-8 w-8 text-amber-400 dark:text-amber-500" />
                <h3 className="font-display text-3xl tracking-tightest">
                  Message received.
                </h3>
                <p className="text-paper-50/70 dark:text-ink-900/70">
                  Thank you &mdash; I&rsquo;ll be in touch within 24 hours.
                </p>
              </motion.div>
            ) : (
              <div className="space-y-5">
                <div>
                  <label
                    htmlFor="name"
                    className="mb-2 block text-xs uppercase tracking-[0.2em] text-paper-50/60 dark:text-ink-900/60"
                  >
                    Name
                  </label>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    value={formData.name}
                    onChange={handleChange}
                    className={`w-full border-b bg-transparent py-3 text-lg text-paper-50 placeholder-paper-50/30 focus:outline-none dark:text-ink-900 dark:placeholder-ink-900/30 ${
                      errors.name
                        ? "border-red-400"
                        : "border-paper-50/20 focus:border-amber-400 dark:border-ink-900/20 dark:focus:border-amber-500"
                    }`}
                    placeholder="Your name"
                  />
                  {errors.name && (
                    <p className="mt-1 text-xs text-red-400">{errors.name}</p>
                  )}
                </div>

                <div>
                  <label
                    htmlFor="email"
                    className="mb-2 block text-xs uppercase tracking-[0.2em] text-paper-50/60 dark:text-ink-900/60"
                  >
                    Email
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={`w-full border-b bg-transparent py-3 text-lg text-paper-50 placeholder-paper-50/30 focus:outline-none dark:text-ink-900 dark:placeholder-ink-900/30 ${
                      errors.email
                        ? "border-red-400"
                        : "border-paper-50/20 focus:border-amber-400 dark:border-ink-900/20 dark:focus:border-amber-500"
                    }`}
                    placeholder="you@company.com"
                  />
                  {errors.email && (
                    <p className="mt-1 text-xs text-red-400">{errors.email}</p>
                  )}
                </div>

                <div>
                  <label
                    htmlFor="message"
                    className="mb-2 block text-xs uppercase tracking-[0.2em] text-paper-50/60 dark:text-ink-900/60"
                  >
                    Project
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows={4}
                    value={formData.message}
                    onChange={handleChange}
                    className={`w-full resize-none border-b bg-transparent py-3 text-lg text-paper-50 placeholder-paper-50/30 focus:outline-none dark:text-ink-900 dark:placeholder-ink-900/30 ${
                      errors.message
                        ? "border-red-400"
                        : "border-paper-50/20 focus:border-amber-400 dark:border-ink-900/20 dark:focus:border-amber-500"
                    }`}
                    placeholder="Tell me what you're building..."
                  />
                  {errors.message && (
                    <p className="mt-1 text-xs text-red-400">{errors.message}</p>
                  )}
                </div>

                <motion.button
                  type="submit"
                  disabled={isSubmitting}
                  whileHover={{ y: -2 }}
                  whileTap={{ scale: 0.97 }}
                  className="inline-flex items-center gap-2 rounded-full bg-amber-400 px-8 py-4 font-medium text-ink-950 transition-colors duration-200 hover:bg-amber-300 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {isSubmitting ? (
                    <>
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-ink-950 border-t-transparent" />
                      <span>Sending...</span>
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4" />
                      <span>Send message</span>
                    </>
                  )}
                </motion.button>
              </div>
            )}
          </motion.form>
        </div>
      </div>
    </section>
  );
};

export default Contact;
