#include <memory>
class Interpolator;
using InterpolatorPtr = std::shared_ptr<Interpolator>; 

#ifndef INTERPOLATOR_H
#define INTERPOLATOR_H

#include <glm/glm.hpp>

class Interpolator {
public:
  virtual ~Interpolator () {}
  virtual glm::vec3 Interpolate (float t) = 0;
};

#endif