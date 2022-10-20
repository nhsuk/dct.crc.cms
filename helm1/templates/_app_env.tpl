{{- define "dct-application.env-app-variables" -}}
env:
  {{- range $key, $val := .Values.envAppVariables }}
  - name: {{ $key | quote }}
    value: {{ $val | quote }}
  {{- end }}
  - name: AUTOWRAPT_BOOTSTRAP
    value: instana
  - name: INSTANA_AGENT_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
{{- end }}
{{- define "dct-application.env-initializer-variables" -}}
env:
  {{- range $key, $val := .Values.envInitializerVariables }}
  - name: {{ $key | quote }}
    value: {{ $val | quote }}
  {{- end }}
  - name: AUTOWRAPT_BOOTSTRAP
    value: instana
  - name: INSTANA_AGENT_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
{{- end }}
{{- define "dct-application.env-delayed-job-variables" -}}
env:
  {{- range $key, $val := .Values.envDelayedJobVariables }}
  - name: {{ $key | quote }}
    value: {{ $val | quote }}
  {{- end }}
  - name: AUTOWRAPT_BOOTSTRAP
    value: instana
  - name: INSTANA_AGENT_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
{{- end }}
{{- define "dct-application.env-sidekiq-variables" -}}
env:
  {{- range $key, $val := .Values.envSidekiqVariables }}
  - name: {{ $key | quote }}
    value: {{ $val | quote }}
  {{- end }}
  - name: AUTOWRAPT_BOOTSTRAP
    value: instana
  - name: INSTANA_AGENT_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
{{- end }}
{{- define "dct-application.env-clockwork-variables" -}}
env:
  {{- range $key, $val := .Values.envClockworkVariables }}
  - name: {{ $key | quote }}
    value: {{ $val | quote }}
  {{- end }}
  - name: AUTOWRAPT_BOOTSTRAP
    value: instana
  - name: INSTANA_AGENT_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
{{- end }}
{{- define "dct-application.env-celery-variables" -}}
env:
  {{- range $key, $val := .Values.envCeleryVariables }}
  - name: {{ $key | quote }}
    value: {{ $val | quote }}
  {{- end }}
  - name: AUTOWRAPT_BOOTSTRAP
    value: instana
  - name: INSTANA_AGENT_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
{{- end }}
