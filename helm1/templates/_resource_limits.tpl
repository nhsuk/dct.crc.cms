{{/* Common HPa resources limits used across helm charts */}}
{{- define "charts.resources-limits" -}}
resources:
  requests:
    memory: {{ .Values.requestsmemory }}
    cpu: {{ .Values.requestscpu }}
  limits:
    memory: {{ .Values.limitsmemory }}
    cpu: {{ .Values.limitscpu }}
{{- end }}
