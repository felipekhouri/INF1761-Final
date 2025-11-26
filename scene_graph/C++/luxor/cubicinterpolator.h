#include <memory>
class CubicInterpolator;
using CubicInterpolatorPtr = std::shared_ptr<CubicInterpolator>; 

#ifndef CUBIC_INTERPOLATOR_H
#define CUBIC_INTERPOLATOR_H

#include "interpolator.h"
#include <glm/glm.hpp>

class CubicInterpolator : public Interpolator {
  glm::vec3 m_p0;
  glm::vec3 m_m0;
  glm::vec3 m_p1;
  glm::vec3 m_m1;
protected:
  CubicInterpolator (const glm::vec3& p0, const glm::vec3& m0, const glm::vec3& p1, const glm::vec3& m1);
public:
  static CubicInterpolatorPtr Make (const glm::vec3& p0, const glm::vec3& m0, const glm::vec3& p1, const glm::vec3& m1);
  virtual ~CubicInterpolator ();
  virtual glm::vec3 Interpolate (float t);
};

#endif