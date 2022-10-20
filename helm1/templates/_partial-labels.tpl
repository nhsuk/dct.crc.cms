{{/* Common labels used across helm charts */}}
{{- define "charts.labels" -}}
name: {{ .Values.labelName | quote }}
owner: {{ .Values.labelOwner | quote }}
costcode: {{ .Values.labelCostCode | quote }}
type: {{ .Values.labelType | quote }}
org: {{ .Values.labelOrg | quote }}
env: {{ .Values.appEnv | quote }}
{{- end }}
