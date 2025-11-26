#version 410

in vec3 veye;
in vec3 neye;
in vec3 light;
in vec2 ftexcoord;

out vec4 fcolor;

uniform vec4 mamb, mdif, mspe;
uniform vec4 lamb, ldif, lspe;
uniform float mshi;

// Texturas
uniform sampler2D decal;
uniform sampler2D bumpTex;

// Flags de efeitos
uniform bool useFog;
uniform bool useBump;

// Parâmetros de fog
uniform vec3 fogColor;

void main(void) {
    vec3 N = normalize(neye);
    vec3 L = normalize(light);
    vec3 V = normalize(-veye);

    // === BUMP MAPPING (rugosidade) ===
    if (useBump) {
        // Pega altura do bump map
        float h = texture(bumpTex, ftexcoord).r;
        float scale = 0.05;

        // Calcula derivadas para perturbar a normal
        vec3 dpdx = dFdx(vec3(ftexcoord, h * scale));
        vec3 dpdy = dFdy(vec3(ftexcoord, h * scale));
        vec3 normalBump = normalize(cross(dpdx, dpdy));

        // Mistura a normal perturbada com a original
        N = normalize(mix(N, normalBump, 0.5));
    }

    vec3 R = reflect(-L, N);

    // === ILUMINAÇÃO PHONG ===
    // ambiente + difusa
    vec4 color = mamb * lamb + mdif * ldif * max(dot(N, L), 0.0);

    // especular (se a superfície está voltada para a luz)
    if (dot(N, L) > 0.0)
        color += mspe * lspe * pow(max(dot(R, V), 0.0), mshi);

    // Multiplica pela textura (apenas RGB, preserva alpha do material)
    vec4 texColor = texture(decal, ftexcoord);
    color.rgb = color.rgb * texColor.rgb;
    color.a = mdif.a;  // Use material diffuse alpha for transparency

    // === FOG (neblina) ===
    if (useFog) {
        float dist = length(veye);
        float fogFactor = exp(-0.3 * dist);  // Aumentado para 0.3 (fog bem mais intenso)
        fogFactor = clamp(fogFactor, 0.0, 1.0);
        color.rgb = mix(fogColor, color.rgb, fogFactor);
        // Keep alpha unchanged for transparency
    }

    fcolor = color;
}
