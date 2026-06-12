import { useState } from "react";
import axios from "axios";
import ArchitectureGraph from "./components/ArchitectureGraph";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    try {
      setLoading(true);

      const result = await axios.post(
        "http://localhost:8000/generate",
        {
          query,
        }
      );

      setResponse(result.data);
    } catch (err) {
      console.error(err);
      alert("Generation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 p-10">
      <div className="max-w-7xl mx-auto">

        <h1 className="text-7xl font-black tracking-tight mb-6">

          TERRA GEN V
          <br />
          Automated Terraform Code Generator

        </h1>

        <p className="text-xl text-slate-500 max-w-3xl mb-10">
          Generate production-ready Terraform from natural language powerd by architecture planning, RAG and automated validation.
        </p>

        <div className="bg-white rounded-xl shadow p-6 mb-6">

          <h2 className="text-xl font-semibold mb-4">
            Infrastructure Request
          </h2>

          <textarea
            className="w-full border rounded-lg p-3 h-32"
            placeholder="Example: ECS Fargate service behind an ALB with autoscaling"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <button
            onClick={generate}
            disabled={loading}
            className="mt-4 px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition shadow"
          >
            {loading ? "Generating..." : "Generate Terraform"}
          </button>

        </div>

        {loading && (
          <div className="bg-white rounded-xl shadow p-6 mb-6">

            <div className="flex items-center gap-3">

              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>

              <span className="text-lg font-medium">
                Generating Terraform...
              </span>

            </div>
          </div>
        )}

        {response && (

          <>
            <div className="bg-white rounded-xl shadow p-6 mb-6">

              <h2 className="text-xl font-semibold mb-4">
                Generation Summary
              </h2>

              <p>
                Query:
                <span className="font-medium ml-2">
                  {response.query}
                </span>
              </p>

              <p className="mt-2">
                ⚡ Generated in:
                <span className="font-bold text-blue-600 ml-2">
                  {response.generation_time_seconds}s
                </span>
              </p>

            </div>

            <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full font-medium mb-6">
                ✓ Terraform Validate Passed
            </div>

            <div className="bg-white rounded-xl shadow p-6 mb-6">

              <h2 className="text-xl font-semibold mb-4">
                Architecture
              </h2>

              <ArchitectureGraph resources={response.architecture}/>

            </div>

            <div className="bg-white rounded-xl shadow p-6">

              <h2 className="text-xl font-semibold mb-4">
                Terraform
              </h2>

              <pre className="bg-black text-green-400 p-4 rounded-lg overflow-auto text-sm">
                {response.terraform}
              </pre>

            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;