#include "luxor.h"
#include "mesh.h"
#include "material.h"
#include "transform.h"
#include "luxorengine.h"

#include <iostream>

Luxor::Luxor ()
{
  MeshPtr base_a = Mesh::Make("../../luxor/base_a.msh");
  MeshPtr base_b = Mesh::Make("../../luxor/base_b.msh");
  MeshPtr haste1 = Mesh::Make("../../luxor/haste1.msh");
  MeshPtr haste2 = Mesh::Make("../../luxor/haste2.msh");
  MeshPtr haste3_a = Mesh::Make("../../luxor/haste3_a.msh");
  MeshPtr haste3_b = Mesh::Make("../../luxor/haste3_b.msh");
  MeshPtr cupula_a = Mesh::Make("../../luxor/cupula_a.msh");
  MeshPtr cupula_b = Mesh::Make("../../luxor/cupula_b.msh");
  MeshPtr lampada = Mesh::Make("../../luxor/lampada.msh");
  MaterialPtr red = Material::Make(1.0f,0.0f,0.0f);
  MaterialPtr white = Material::Make(1.0f,1.0f,1.0f);
  white->SetAmbient(1.0f,1.0f,1.0f);
  TransformPtr trf_all = Transform::Make();
  TransformPtr trf_base = Transform::Make();
  TransformPtr trf_haste1 = Transform::Make();
  TransformPtr trf_haste2 = Transform::Make();
  TransformPtr trf_haste3 = Transform::Make();
  TransformPtr trf_cupula = Transform::Make();
  TransformPtr trf_lampada = Transform::Make();
  trf_haste1->Translate(0.0f,4.0f,0.0f);
  trf_haste2->Translate(0.0f,17.15f,0.0f);
  trf_haste3->Translate(0.0f,16.78f,0.0f);
  trf_cupula->Translate(0.0f,18.12f,0.0f);
  trf_lampada->Translate(0.0f,8.4f,9.0f);
  m_light_node = Node::Make(trf_lampada,{white},{lampada});
  m_node = Node::Make(trf_all,{red},{
    Node::Make(trf_base,{base_a,base_b},{
      Node::Make(trf_haste1,{haste1},{
        Node::Make(trf_haste2,{haste2},{
          Node::Make(trf_haste3,{haste3_a,haste3_b},{
            Node::Make(trf_cupula,{cupula_a,cupula_b},{
              m_light_node
            })
          })
        })
      })
    })
  });
  m_engine = LuxorEngine::Make(trf_all,trf_base,trf_haste1,trf_haste2,trf_haste3,trf_cupula,trf_lampada);
}

LuxorPtr Luxor::Make ()
{
  return LuxorPtr(new Luxor());
}

Luxor::~Luxor ()
{
}

NodePtr Luxor::GetNode ()
{
  return m_node;
}

NodePtr Luxor::GetLightNode ()
{
  return m_light_node;
}

LuxorEnginePtr Luxor::GetEngine ()
{
  return m_engine;
}