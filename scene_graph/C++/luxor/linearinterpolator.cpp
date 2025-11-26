#include "linearinterpolator.h"
LinearInterpolator::LinearInterpolator (const glm::vec3& p0, const glm::vec3& p1)
: m_p0(p0), m_p1(p1)
{
}
LinearInterpolatorPtr LinearInterpolator::Make (const glm::vec3& p0, const glm::vec3& p1)
{
  return LinearInterpolatorPtr(new LinearInterpolator(p0,p1));
}

LinearInterpolator::~LinearInterpolator ()
{
}

glm::vec3 LinearInterpolator::Interpolate (float t)
{
  return (1.0f-t) * m_p0 + t * m_p1;
}
