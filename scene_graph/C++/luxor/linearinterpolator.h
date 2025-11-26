#include <memory>
class LinearInterpolator;
using LinearInterpolatorPtr = std::shared_ptr<LinearInterpolator>; 

#ifndef LINEAR_INTERPOLATOR_H
#define LINEAR_INTERPOLATOR_H

#include "interpolator.h"
#include <glm/glm.hpp>

class LinearInterpolator : public Interpolator {
  glm::vec3 m_p0;
  glm::vec3 m_p1;
protected:
  LinearInterpolator (const glm::vec3& p0, const glm::vec3& p1);
public:
  static LinearInterpolatorPtr Make (const glm::vec3& p0, const glm::vec3& p1);
  virtual ~LinearInterpolator ();
  virtual glm::vec3 Interpolate (float t);
};

#endif