#include <memory>
class Luxor;
using LuxorPtr = std::shared_ptr<Luxor>; 

#ifndef LUXO_H
#define LUXO_H

#include "node.h"
#include "luxorengine.h"

class Luxor 
{
  NodePtr m_node;
  NodePtr m_light_node;
  LuxorEnginePtr m_engine;
protected:
  Luxor ();
public:
  virtual ~Luxor ();
  static LuxorPtr Make ();
  NodePtr GetNode ();
  NodePtr GetLightNode ();
  LuxorEnginePtr GetEngine ();
};

#endif