import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {

  const [query, setQuery] = useState("");

  const navigate = useNavigate();

  return (

    <div className="min-h-screen bg-slate-100">

      <div className="max-w-5xl mx-auto px-6 pt-24">

        <h1 className="text-5xl font-black tracking-tight mb-6">

          TERRA GEN V

          <br />

          Automated Terraform Code Generator

        </h1>

        <p className="text-xl text-slate-500 max-w-3xl mb-10">

          Generate production-ready Terraform from natural language powered by architecture planning, RAG and automated validation.

        </p>

        <div className="bg-white rounded-2xl shadow-xl p-8">

          <textarea
            className="w-full border rounded-xl p-4 h-40"
            value={query}
            placeholder="Example: ECS Fargate service behind an ALB with autoscaling"
            onChange={(e) =>
              setQuery(e.target.value)
            }
          />

          <button
            className="mt-6 px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700"
            onClick={() =>
              navigate("/results", {
                state: {
                  query,
                },
              })
            }
          >
            Generate Architecture
          </button>

        </div>

      </div>

    </div>
  );
}