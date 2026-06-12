import ReactFlow, {
  Background,
  Controls,
} from "reactflow";

import type {
  Node,
  Edge,
} from "reactflow";

import "reactflow/dist/style.css";

type Props = {
  resources: string[];
};

export default function ArchitectureGraph({
  resources,
}: Props) {

  const nodes: Node[] = resources.map(
    (resource, index) => ({
      id: String(index),

      data: {
        label: resource,
      },

      position: {
        x: 250,
        y: index * 100,
      },
    })
  );

  const edges: Edge[] = [];

  for (let i = 0; i < resources.length - 1; i++) {

    edges.push({
      id: `e${i}-${i + 1}`,
      source: String(i),
      target: String(i + 1),
    });

  }

  return (

    <div
      style={{
        width: "100%",
        height: "600px",
      }}
    >

      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
      >

        <Background />
        <Controls />

      </ReactFlow>

    </div>

  );
}