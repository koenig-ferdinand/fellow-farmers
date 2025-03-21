import React, { useState } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import FarmForm from "@/components/FarmForm";
import ActionPlan from "@/components/ActionPlan";
import ChartSection from "@/components/ChartSection";
import Header from "@/components/Header";
import FieldSizeSelector from "@/components/FieldSizeSelector"; // Stub
import { useToast } from "@/components/ui/use-toast";
import { Droplet, Sprout, Package, Bug } from "lucide-react";
import { calculateDetailedStress, getWeatherData } from "@/services/api";

/** Minimal i18n approach for language toggle */
const translations = {
  en: {
    farmDetailsTitle: "Enter Your Farm Details",
    analysisTitle: "Field Analysis & Recommendations",
    selectedAnalysisTitle: "Selected Analysis",
    hideBelowUntilSubmit:
      "No analysis data yet. Please fill out the form above.",
    excitedTitle: "Excited for more?",
    excitedSubtitle: "Choose an option to explore:",
    bubbleFarmers: "Fellow Farmers",
    bubbleExperts: "Experts",
    bubbleIdeas: "New Ideas",
    analysisComplete: "Analysis Complete",
    analysisDesc: "Successfully analyzed your farm data.",
    analysisFail: "Analysis Failed",
    analysisFailDesc: "Something went wrong. Please try again.",
  },
  de: {
    farmDetailsTitle: "Geben Sie Ihre Felddaten ein",
    analysisTitle: "Feldanalyse & Empfehlungen",
    selectedAnalysisTitle: "Ausgewählte Analysen",
    hideBelowUntilSubmit:
      "Noch keine Analysedaten. Bitte füllen Sie das Formular aus.",
    excitedTitle: "Neugierig auf mehr?",
    excitedSubtitle: "Wählen Sie eine Option:",
    bubbleFarmers: "Mitbauern",
    bubbleExperts: "Experten",
    bubbleIdeas: "Neue Ideen",
    analysisComplete: "Analyse abgeschlossen",
    analysisDesc: "Ihre Felddaten wurden erfolgreich analysiert.",
    analysisFail: "Analyse fehlgeschlagen",
    analysisFailDesc:
      "Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut.",
  },
};

// Data for the corner boxes
const boxData = [
  {
    key: "soil",
    title: "Soil Health",
    icon: <Sprout className="h-6 w-6 text-green-600" />,
    color: "text-plant-green-core",
    summary: "Maintain optimal pH, apply compost as needed.",
  },
  {
    key: "water",
    title: "Water Management",
    icon: <Droplet className="h-6 w-6 text-blue-600" />,
    color: "text-air-blue-core",
    summary: "Irrigate every 3 days; track moisture levels.",
  },
  {
    key: "disease",
    title: "Disease & Pests",
    icon: <Bug className="h-6 w-6 text-red-600" />,
    color: "text-red-700",
    summary: "Monitor for leaf spots; consider preventive sprays.",
  },
  {
    key: "products",
    title: "Recommended Products",
    icon: <Package className="h-6 w-6 text-sun-orange-mid" />,
    color: "text-sun-orange-mid",
    summary: "Bio-Fertilizer XL to enhance root development.",
  },
];

interface BoxData {
  key: string;
  title: string;
  icon: JSX.Element;
  color: string;
  summary: string;
}

interface CornerBoxProps {
  data: BoxData;
  onSelectBox: (key: string) => void;
  selected: boolean;
}

const CornerBox: React.FC<CornerBoxProps> = ({
  data,
  onSelectBox,
  selected,
}) => {
  return (
    <div
      className={`cursor-pointer transition-all hover:shadow-md p-4 border rounded-md ${
        selected ? "border-air-blue-core" : "border-transparent"
      }`}
      onClick={() => onSelectBox(data.key)}
    >
      <div className="flex items-center justify-between mb-2">
        <h3
          className={`text-xl font-semibold flex items-center gap-2 ${data.color}`}
        >
          {data.icon} {data.title}
        </h3>
      </div>
      <p className="text-base text-gray-600">{data.summary}</p>
    </div>
  );
};

// Parallax background
const BackLayer: React.FC = () => {
  const { scrollY } = useScroll();
  // Move slower than main content
  const layerY = useTransform(scrollY, [0, 1000], [0, -200]);

  return (
    <motion.div
      className="pointer-events-none fixed inset-0 z-0"
      style={{
        y: layerY,
        background:
          "radial-gradient(circle at 20% 30%, rgba(0, 157, 220, 0.07) 0%, transparent 20%), radial-gradient(circle at 80% 70%, rgba(76, 154, 42, 0.07) 0%, transparent 20%)",
        opacity: 0.7,
      }}
    />
  );
};

const Index: React.FC = () => {
  const { toast } = useToast();

  // Language toggle
  const [lang, setLang] = useState<"en" | "de">("en");
  const toggleLang = () => setLang((prev) => (prev === "en" ? "de" : "en"));

  // Form/analysis states
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<any | null>(null);
  const [weatherData, setWeatherData] = useState<any | null>(null);
  const [selectedBoxes, setSelectedBoxes] = useState<string[]>([]);

  // Show/hide sections
  const [showPostFormSections, setShowPostFormSections] = useState(false);

  // Parallax for form
  const { scrollY } = useScroll();
  const formTranslateY = useTransform(scrollY, [0, 300], [0, -150]);

  /** Handle form submission */
  const handleSubmit = async (data: any) => {
    setIsLoading(true);
    try {
      // Mock API calls
      const result = await calculateDetailedStress(data);
      const weather = data.location.trim()
        ? await getWeatherData(data.location)
        : null;

      setAnalysisResults(result);
      setWeatherData(weather);

      toast({
        title: translations[lang].analysisComplete,
        description: translations[lang].analysisDesc,
      });

      setShowPostFormSections(true);
    } catch (err) {
      console.error(err);
      toast({
        title: translations[lang].analysisFail,
        description: translations[lang].analysisFailDesc,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectBox = (key: string) => {
    setSelectedBoxes((prev) =>
      prev.includes(key) ? prev.filter((item) => item !== key) : [...prev, key]
    );
  };

  const handleBubbleClick = (bubble: string) => {
    console.log(`Navigating to: ${bubble}`);
  };

  return (
    <div className="flex flex-col min-h-screen font-poppins text-gray-800 overflow-x-hidden">
      <BackLayer />
      <Header />

      {/* MAIN CONTENT */}
      <main className="flex-1 relative">
        {/* Language Toggle Button */}
        <button
          className="absolute top-4 right-4 z-50 bg-white px-3 py-1 rounded shadow text-sm font-medium"
          onClick={toggleLang}
        >
          {lang === "en" ? "Switch to DE" : "Switch to EN"}
        </button>

        {/* FARM FORM SECTION */}
        <motion.section
          className="relative z-10 px-4 max-w-4xl mx-auto mt-8"
          style={{ y: formTranslateY }}
        >
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-3xl font-bold mb-4 text-gray-700">
              {translations[lang].farmDetailsTitle}
            </h2>
            <FarmForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>
        </motion.section>

        {/* Only show the rest if the form was submitted */}
        {showPostFormSections && (
          <>
            {/* ANALYSIS SECTION */}
            <section className="py-12 bg-gray-50">
              <div className="container mx-auto px-4 max-w-5xl">
                {analysisResults ? (
                  <div className="bg-white rounded-lg shadow p-6 md:p-8">
                    <h2 className="text-3xl font-bold mb-6 text-gray-800">
                      {translations[lang].analysisTitle}
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {boxData.map((box) => (
                        <CornerBox
                          key={box.key}
                          data={box}
                          onSelectBox={handleSelectBox}
                          selected={selectedBoxes.includes(box.key)}
                        />
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-gray-400 py-8">
                    <p>{translations[lang].hideBelowUntilSubmit}</p>
                  </div>
                )}
              </div>
            </section>

            {/* SELECTED BOXES */}
            {selectedBoxes.length > 0 && (
              <section className="py-12 bg-white">
                <div className="container mx-auto px-4 max-w-5xl">
                  <h2 className="text-3xl font-bold text-gray-800 mb-6">
                    {translations[lang].selectedAnalysisTitle}
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {boxData
                      .filter((box) => selectedBoxes.includes(box.key))
                      .map((box) => (
                        <ChartSection
                          key={box.key}
                          title={`${box.title} Details`}
                        />
                      ))}
                  </div>
                </div>
              </section>
            )}

            {/* ACTION PLAN */}
            <ActionPlan selectedBoxes={selectedBoxes} />

            {/* FINAL EXCITED FOR MORE SECTION */}
            <section className="py-12 bg-gray-50">
              <div className="container mx-auto px-4 max-w-5xl">
                <h2 className="text-3xl font-bold text-gray-800 mb-2">
                  {translations[lang].excitedTitle}
                </h2>
                <p className="text-lg text-gray-600 mb-6">
                  {translations[lang].excitedSubtitle}
                </p>
                <div className="flex flex-wrap gap-6">
                  <div
                    className="flex-1 min-w-[200px] bg-white p-6 rounded shadow cursor-pointer hover:shadow-lg transition"
                    onClick={() => handleBubbleClick("fellowFarmers")}
                  >
                    <h3 className="text-2xl font-semibold text-gray-800 mb-2">
                      {translations[lang].bubbleFarmers}
                    </h3>
                    <p className="text-sm text-gray-600">
                      Connect with local farmers to share experiences.
                    </p>
                  </div>
                  <div
                    className="flex-1 min-w-[200px] bg-white p-6 rounded shadow cursor-pointer hover:shadow-lg transition"
                    onClick={() => handleBubbleClick("experts")}
                  >
                    <h3 className="text-2xl font-semibold text-gray-800 mb-2">
                      {translations[lang].bubbleExperts}
                    </h3>
                    <p className="text-sm text-gray-600">
                      Get insights from agronomy experts in your region.
                    </p>
                  </div>
                  <div
                    className="flex-1 min-w-[200px] bg-white p-6 rounded shadow cursor-pointer hover:shadow-lg transition"
                    onClick={() => handleBubbleClick("newIdeas")}
                  >
                    <h3 className="text-2xl font-semibold text-gray-800 mb-2">
                      {translations[lang].bubbleIdeas}
                    </h3>
                    <p className="text-sm text-gray-600">
                      Discover new plant varieties and suggestions for your
                      area.
                    </p>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}
      </main>

      {/* FOOTER */}
      <footer className="bg-gray-900 py-4 text-center text-sm text-white">
        &copy; {new Date().getFullYear()} Syngenta Biologicals – Innovation
        powered by nature
      </footer>
    </div>
  );
};

export default Index;
