
#include "cubicinterpolator.h"

CubicInterpolator::CubicInterpolator (const glm::vec3& p0, const glm::vec3& m0, const glm::vec3& p1, const glm::vec3& m1)
: m_p0(p0), m_m0(m0), m_p1(p1), m_m1(m1)
{
}
CubicInterpolatorPtr CubicInterpolator::Make (const glm::vec3& p0, const glm::vec3& m0, const glm::vec3& p1, const glm::vec3& m1)
{
  return CubicInterpolatorPtr(new CubicInterpolator(p0,m0,p1,m1));
}

CubicInterpolator::~CubicInterpolator ()
{
}
glm::vec3 CubicInterpolator::Interpolate (float t)
{
  float t2 = t*t;
  float t3 = t*t2;
  return (2*t3-3*t2+1) * m_p0 +
         (t3-2*t2+t) * m_m0 + 
         (-2*t3+3*t2) * m_p1 +
         (t3-t2) * m_m1;
}
