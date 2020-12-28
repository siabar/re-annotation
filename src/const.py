REQUIRED_HEADERS = ["SECCION_DIAGNOSTICO_PRINCIPAL", "SECCION_DIAGNOSTICOS"]

REQUIRED_MAIN_VARIABLES = ["Ictus_isquemico", "Ataque_isquemico_transitorio", "Hemorragia_cerebral"]

REQUIRED_SECOND_VARIABLES = ["Arteria_afectada", "Localizacion", "Lateralizacion", "Etiologia"]

REQUIRED_SECOND_VARIABLES_FIRST = ["Lateralizacion", "Etiologia"]

HEMORRAGIA_EVIDENCE = []
ISQUEMICO_EVIDENCE = []

CARMEN_ISABEL = ["Trombolisis_intravenosa", "Trombectomia_mecanica", "Trombolisis_intraarterial", "TAC_craneal",
                 "Test_de_disfagia",
                 "Fecha_trombolisis_rtPA", "Fecha_inicio_trombectomia", "Fecha_primera_serie_trombectomia",
                 "Fecha_recanalizacion", "Fecha_fin_trombectomia", "Fecha_inicio_trombolisis_intraarterial",
                 "Fecha_TAC",
                 "Hora_primer_bolus_trombolisis_rtPA", "Hora_inicio_trombectomia", "Hora_primera_serie_trombectomia",
                 "Hora_recanalizacion", "Hora_fin_trombectomia", "Hora_inicio_trombolisis_intraarterial", "Hora_TAC",
                 "Tiempo_puerta_puncion", "Tiempo_puerta_aguja"]

EUGENIA = ["Ictus_isquemico", "Ataque_isquemico_transitorio", "Hemorragia_cerebral",
           "Arteria_afectada", "Localizacion", "Lateralizacion", "Etiologia",
           "Fecha_de_ingreso", "Fecha_de_alta", "Hora_de_alta", "Fecha_llegada_hospital", "Hora_llegada_hospital",
           "Fecha_inicio_sintomas", "Hora_inicio_sintomas"]

VICTORIA = ["Tratamiento_anticoagulante", "Tratamiento_antiagregante",
            "Tratamiento_anticoagulante_hab", "Tratamiento_antiagregante_hab",
            "mRankin", "mRankin_previa", "mRankin_alta",
            "NIHSS", "NIHSS_previa", "NIHSS_alta", "ASPECTS",
            "Tratamiento_anticoagulante_alta", "Tratamiento_antiagregante_alta"]

FECHA_HORA_TIEMO = ["HORA", "FECHA", "TIEMPO"]

EVIDENCE_CARMEN_ISABLE = ["Fecha_trombolisis_rtPA", "Hora_primer_bolus_trombolisis_rtPA",
                            "Fecha_fin_trombectomia", "Hora_fin_trombectomia",
                            "Fecha_primera_serie_trombectomia", "Hora_primera_serie_trombectomia",
                            "Fecha_inicio_trombectomia", "Hora_inicio_trombectomia",
                            "Fecha_inicio_trombolisis_intraarterial", "Hora_inicio_trombolisis_intraarterial"]
