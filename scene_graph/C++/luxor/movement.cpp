#include "movement.h"

Movement::Movement (float T)
: m_t(0.0f), m_T(T)
{
}

MovementPtr Movement::Make (float T)
{
  return MovementPtr(new Movement(T));
}

Movement::~Movement ()
{
}

void Movement::AddTranslation (TransformPtr trf, InterpolatorPtr interp)
{
  m_trl_trf.push_back(trf);
  m_trl_interp.push_back(interp);
}

void Movement::AddRotation (TransformPtr trf, InterpolatorPtr interp)
{
  m_rot_trf.push_back(trf);
  m_rot_interp.push_back(interp);
}

bool Movement::Advance (float dt, bool reverse)
{
  float t = m_t + dt;
  if (t > m_T) {
    t = m_T;
  }
  float t0 = reverse ? (m_T-m_t)/m_T : m_t/m_T;
  float t1 = reverse ? (m_T-t)/m_T : t/m_T;
  // perform translations
  for (int i=0; i<m_trl_trf.size(); ++i) {
    glm::vec3 v0 = m_trl_interp[i]->Interpolate(t0);
    glm::vec3 v1 = m_trl_interp[i]->Interpolate(t1);
    m_trl_trf[i]->Translate(v1[0]-v0[0],v1[1]-v0[1],v1[2]-v0[2]);
  }
  // perform rotations 
  for (int i=0; i<m_rot_trf.size(); ++i) {
    glm::vec3 v0 = m_rot_interp[i]->Interpolate(t0);
    glm::vec3 v1 = m_rot_interp[i]->Interpolate(t1);
    m_rot_trf[i]->Rotate(v1[0]-v0[0],1.0f,0.0f,0.0f);
    m_rot_trf[i]->Rotate(v1[1]-v0[1],0.0f,1.0f,0.0f);
    m_rot_trf[i]->Rotate(v1[2]-v0[2],0.0f,0.0f,1.0f);
  }
  if (t == m_T) {  // check if movement ended
    m_t = 0.0f;    // reset internal clock
    return true;   // signalize the movement ended after this advance
  }
  else {
    m_t = t;
    return false;  // signalize the movement continues
  }
}
