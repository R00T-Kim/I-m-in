# Paper Writing Plan

## Writing Order (Sequential)

Based on mucamp1 methodology:

1. **Related Works** — 관련 연구 정리
2. **Proposed Method** — 제안 방법 (제로샷 펌웨어 분석 방법론)
3. **Experimental Results** — 실험 결과 (Vgate iCar Pro 2S 케이스)
4. **Introduction** — 서론 (배경 및 동기)
5. **Conclusion** — 결론 (기여 및 향후 과제)
6. **Abstract** — 초록 (마지막)

---

## References

### Related Works Categories

1. **Threat Intelligence & Attack Detection**
   - ThreatInsight (Wang et al., 2024): 위협 인텔리전스 기반 조기 탐지
   - Cyberattack event logs (Alzu'bi et al., 2025): 딥러닝 + 시맨틱 분석
   - AI-based CTI (Spyros et al., 2025): 위협 인텔리전스 관리 프레임워크

2. **LLM/AI-driven Security Analysis**
   - AttacKG+ (Zhang et al., 2025): LLM으로 공격 그래프 구축

3. **Data Augmentation & Generative Models**
   - SMOTE (Chawla et al., 2002): 소수 클래스 오버샘플링
   - Seq2Seq (Sutskever et al., 2014): 시퀀스 생성 모델
   - SeqGAN (Yu et al., 2017): GAN 기반 시퀀스 생성
   - Password generation (Biesner et al., 2020): 생성 딥러닝
   - IoT-23 cyberattacks (Abdalgawad et al., 2021): IoT 공격 탐지

4. **Vulnerability Analysis & Mapping**
   - Gionanidis et al. (2022): 취약점 정보 → ATT&CK 매핑

### Our Contribution

- **Zero-shot firmware format reverse engineering** (문서 없이 패턴 분석)
- Case study: Vgate iCar Pro 2S v2.3.14
- Methodology: record clustering, correlation analysis, protocol inference

### Bibliography

`references.bib` (10 entries)

---

**Note**: Write sequentially; do NOT jump to Abstract first.
