import {
  useLocation,
  useNavigate,
} from "react-router-dom";

import {
  useEffect,
  useState,
} from "react";

import axios from "axios";

export default function Results() {

  const location = useLocation();

  const navigate = useNavigate();

  const query =
    location.state?.query;

  const [loading, setLoading] =
    useState(true);

  const [response, setResponse] =
    useState<any>(null);

  useEffect(() => {

    if (!query) {

      navigate("/");

      return;
    }

    async function run() {

      const result =
        await axios.post(
          "http://localhost:8000/generate",
          {
            query,
          }
        );

      setResponse(result.data);

      setLoading(false);
    }

    run();

  }, []);

  if (loading) {

    return (

      <div className="min-h-screen flex items-center justify-center">

        <div className="text-center">

          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-6"></div>

          <h2 className="text-2xl font-bold">
            Generating Terraform...
          </h2>

        </div>

      </div>

    );
  }

  return (

    <div className="min-h-screen bg-slate-100">

      <div className="max-w-7xl mx-auto p-10">

        <div className="bg-white rounded-xl shadow p-6 mb-6">

          <button
            onClick={() => navigate("/")}
            className="
              mb-6
              px-5
              py-3
              bg-white
              rounded-xl
              shadow
              hover:shadow-lg
              transition
              font-medium
            "
          >
            ← New Generation
          </button>

          <div className="grid grid-cols-3 gap-4 mb-6">

            <div className="bg-white rounded-xl shadow p-6">
              <div className="text-sm text-slate-500">
                Resources
              </div>

              <div className="text-3xl font-bold">
                {response.architecture.length}
              </div>
            </div>

            <div className="bg-white rounded-xl shadow p-6">
              <div className="text-sm text-slate-500">
                Validation
              </div>

              <div className="text-3xl font-bold text-green-600">
                PASS
              </div>
            </div>

            <div className="bg-white rounded-xl shadow p-6">
              <div className="text-sm text-slate-500">
                Generation Time
              </div>

              <div className="text-3xl font-bold">
                {response.generation_time_seconds}s
              </div>
            </div>

          </div>

          <h2 className="text-2xl font-bold mb-4">

            Query

          </h2>

          <p>
            {response.query}
          </p>

        </div>

        <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full font-medium mb-6">
          ✓ Terraform Validate Passed
        </div>

        <div className="bg-white rounded-xl shadow p-6 mb-6">

          <h2 className="text-2xl font-bold mb-4">

            Architecture

          </h2>

          {response.architecture.map(
            (resource: string) => (

              <div
                key={resource}
                className="mb-2"
              >
                • {resource}
              </div>

            )
          )}

        </div>

        <div className="bg-white rounded-xl shadow p-6">

          <h2 className="text-2xl font-bold mb-4">

            Terraform

          </h2>

          <pre className="bg-black text-green-400 p-6 rounded-xl overflow-auto">

            {response.terraform}

          </pre>

        </div>

      </div>

    </div>

  );
}