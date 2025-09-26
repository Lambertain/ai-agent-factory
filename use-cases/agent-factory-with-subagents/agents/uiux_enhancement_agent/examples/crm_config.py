"""
CRM UI/UX конфигурация для UI/UX Enhancement Agent.

Этот файл демонстрирует настройку агента для CRM систем и клиентских платформ.
Включает настройки для управления контактами, продажами и аналитики взаимодействий.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..dependencies import UIUXEnhancementDependencies


@dataclass
class CRMUIUXDependencies(UIUXEnhancementDependencies):
    """Конфигурация для CRM проектов."""

    # Основные настройки
    domain_type: str = "crm"
    project_type: str = "sales_platform"

    # CRM специфичные настройки
    design_system_type: str = "material"  # Material Design для CRM
    css_framework: str = "styled-components"
    ui_framework: str = "react"
    framework_version: str = "18"
    accessibility_level: str = "wcag-aa"
    responsive_strategy: str = "desktop-first"  # CRM часто desktop-first

    # CRM функциональность
    enable_contact_management: bool = True
    enable_lead_tracking: bool = True
    enable_opportunity_pipeline: bool = True
    enable_activity_timeline: bool = True
    enable_email_integration: bool = True
    enable_calendar_integration: bool = True
    enable_reporting_dashboard: bool = True

    # Sales pipeline настройки
    pipeline_stages: List[str] = field(default_factory=lambda: [
        "Lead", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"
    ])

    # UI предпочтения
    enable_kanban_view: bool = True
    enable_list_view: bool = True
    enable_calendar_view: bool = True
    enable_quick_actions: bool = True
    enable_bulk_operations: bool = True

    def __post_init__(self):
        super().__post_init__()

        # CRM knowledge tags
        self.knowledge_tags.extend([
            "crm", "sales", "contacts", "pipeline", "material-design"
        ])

    def get_color_scheme(self) -> Dict[str, str]:
        """CRM-оптимизированная цветовая схема."""
        return {
            # Основные CRM цвета
            "primary": "hsl(233, 87%, 52%)",      # Professional blue
            "secondary": "hsl(270, 95%, 60%)",    # Purple accent
            "accent": "hsl(142, 71%, 45%)",       # Success green
            "background": "hsl(0, 0%, 98%)",      # Light background
            "foreground": "hsl(240, 10%, 4%)",    # Dark text
            "muted": "hsl(240, 4%, 95%)",         # Light gray
            "border": "hsl(240, 6%, 90%)",        # Border gray

            # Pipeline stage colors
            "lead": "hsl(200, 98%, 39%)",         # Blue
            "qualified": "hsl(160, 60%, 45%)",    # Teal
            "proposal": "hsl(38, 92%, 50%)",      # Orange
            "negotiation": "hsl(271, 91%, 65%)",  # Purple
            "closed_won": "hsl(142, 71%, 45%)",   # Green
            "closed_lost": "hsl(0, 84%, 60%)",    # Red

            # Activity types
            "call": "hsl(233, 87%, 52%)",         # Blue
            "email": "hsl(38, 92%, 50%)",         # Orange
            "meeting": "hsl(271, 91%, 65%)",      # Purple
            "task": "hsl(160, 60%, 45%)",         # Teal
            "note": "hsl(240, 6%, 50%)",          # Gray

            # Priority levels
            "priority_high": "hsl(0, 84%, 60%)",     # Red
            "priority_medium": "hsl(38, 92%, 50%)",  # Orange
            "priority_low": "hsl(160, 60%, 45%)",    # Green

            # Status indicators
            "active": "hsl(142, 71%, 45%)",       # Green
            "inactive": "hsl(240, 6%, 50%)",      # Gray
            "overdue": "hsl(0, 84%, 60%)",        # Red
            "upcoming": "hsl(233, 87%, 52%)"      # Blue
        }

    def get_component_config(self) -> Dict[str, Any]:
        """Конфигурация компонентов для CRM."""
        return {
            "contact_card": {
                "show_avatar": True,
                "show_company": True,
                "show_last_interaction": True,
                "show_lead_score": True,
                "show_quick_actions": self.enable_quick_actions,
                "compact_mode": False
            },
            "pipeline_board": {
                "kanban_view": self.enable_kanban_view,
                "drag_and_drop": True,
                "stage_summaries": True,
                "opportunity_cards": True,
                "probability_indicators": True,
                "value_display": True
            },
            "activity_timeline": {
                "chronological_order": True,
                "activity_types": ["call", "email", "meeting", "task", "note"],
                "inline_editing": True,
                "quick_add": True,
                "filter_by_type": True,
                "filter_by_date": True
            },
            "navigation": {
                "sidebar_layout": True,
                "quick_search": True,
                "recent_contacts": True,
                "favorites": True,
                "notifications": True
            },
            "dashboard": {
                "sales_metrics": True,
                "activity_charts": True,
                "pipeline_overview": True,
                "performance_kpis": True,
                "goal_tracking": True,
                "customizable_widgets": True
            },
            "data_tables": {
                "sortable_columns": True,
                "filterable": True,
                "bulk_actions": self.enable_bulk_operations,
                "export_options": ["CSV", "Excel", "PDF"],
                "column_customization": True,
                "saved_views": True
            }
        }

    def get_layout_config(self) -> Dict[str, Any]:
        """Конфигурация layout для CRM."""
        return {
            "grid": {
                "contact_grid": {"desktop": 3, "tablet": 2, "mobile": 1},
                "opportunity_grid": {"desktop": 4, "tablet": 2, "mobile": 1},
                "dashboard_grid": {"desktop": 4, "tablet": 2, "mobile": 1}
            },
            "spacing": {
                "section_gap": "3rem",
                "component_gap": "1.5rem",
                "element_gap": "0.75rem"
            },
            "containers": {
                "header": "full",
                "sidebar": "fixed",
                "main": "fluid",
                "footer": "full"
            },
            "sidebar": {
                "width": "280px",
                "collapsible": True,
                "mini_mode": True,
                "resize_handle": True
            }
        }

    def get_interaction_config(self) -> Dict[str, Any]:
        """Конфигурация взаимодействий для CRM."""
        return {
            "drag_and_drop": {
                "pipeline_stages": True,
                "contact_organization": True,
                "file_uploads": True,
                "visual_feedback": True
            },
            "quick_actions": {
                "keyboard_shortcuts": True,
                "context_menus": True,
                "floating_action_button": True,
                "batch_operations": self.enable_bulk_operations
            },
            "search": {
                "global_search": True,
                "scoped_search": True,
                "autocomplete": True,
                "recent_searches": True,
                "saved_searches": True
            },
            "notifications": {
                "real_time": True,
                "desktop_notifications": True,
                "email_alerts": True,
                "in_app_notifications": True,
                "notification_center": True
            }
        }

    def get_data_visualization_config(self) -> Dict[str, Any]:
        """Конфигурация визуализации данных для CRM."""
        return {
            "charts": {
                "sales_funnel": True,
                "revenue_trends": True,
                "activity_heatmap": True,
                "conversion_rates": True,
                "performance_metrics": True
            },
            "chart_types": [
                "bar", "line", "pie", "donut", "funnel", "scatter", "heatmap"
            ],
            "interactive_features": {
                "drill_down": True,
                "filtering": True,
                "date_range_selection": True,
                "export_options": True
            },
            "real_time_updates": True,
            "responsive_charts": True
        }


# Пример использования
def get_crm_uiux_dependencies() -> CRMUIUXDependencies:
    """Создать конфигурацию для CRM проекта."""
    return CRMUIUXDependencies(
        project_path="/crm/platform",
        project_name="Sales CRM Platform",
        domain_type="crm",
        project_type="sales_platform",
        design_system_type="material",
        enable_contact_management=True,
        enable_lead_tracking=True,
        enable_opportunity_pipeline=True,
        enable_activity_timeline=True
    )


# Пример использования в React компонентах
CRM_COMPONENT_EXAMPLES = {
    "contact_card": """
// CRM Contact Card Component
import { Card, Avatar, Badge, Button } from '@mui/material';
import { Phone, Email, Event, Star } from '@mui/icons-material';

export function CRMContactCard({ contact, config }) {
  const colorScheme = config.get_color_scheme();
  const componentConfig = config.get_component_config().contact_card;

  return (
    <Card sx={{ p: 2, mb: 2, position: 'relative' }}>
      {/* Contact Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        {componentConfig.show_avatar && (
          <Avatar
            src={contact.avatar}
            sx={{ width: 48, height: 48, mr: 2 }}
          >
            {contact.firstName?.[0]}{contact.lastName?.[0]}
          </Avatar>
        )}

        <Box sx={{ flex: 1 }}>
          <Typography variant="h6" component="h3">
            {contact.firstName} {contact.lastName}
          </Typography>

          {componentConfig.show_company && contact.company && (
            <Typography variant="body2" color="text.secondary">
              {contact.jobTitle} at {contact.company}
            </Typography>
          )}
        </Box>

        {componentConfig.show_lead_score && (
          <Badge
            badgeContent={contact.leadScore}
            color={contact.leadScore >= 80 ? "success" : "warning"}
            sx={{ mr: 1 }}
          />
        )}
      </Box>

      {/* Contact Details */}
      <Box sx={{ mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Email sx={{ mr: 1, fontSize: 16, color: 'text.secondary' }} />
          <Typography variant="body2">{contact.email}</Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Phone sx={{ mr: 1, fontSize: 16, color: 'text.secondary' }} />
          <Typography variant="body2">{contact.phone}</Typography>
        </Box>
      </Box>

      {/* Last Interaction */}
      {componentConfig.show_last_interaction && contact.lastInteraction && (
        <Box sx={{ mb: 2, p: 1, bgcolor: 'grey.50', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            Last interaction:
          </Typography>
          <Typography variant="body2">
            {contact.lastInteraction.type} - {contact.lastInteraction.date}
          </Typography>
        </Box>
      )}

      {/* Quick Actions */}
      {componentConfig.show_quick_actions && (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            size="small"
            startIcon={<Phone />}
            sx={{ color: colorScheme.call }}
          >
            Call
          </Button>
          <Button
            size="small"
            startIcon={<Email />}
            sx={{ color: colorScheme.email }}
          >
            Email
          </Button>
          <Button
            size="small"
            startIcon={<Event />}
            sx={{ color: colorScheme.meeting }}
          >
            Schedule
          </Button>
        </Box>
      )}
    </Card>
  );
}
""",

    "pipeline_board": """
// CRM Pipeline Board Component
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { Card, Typography, Chip, Box } from '@mui/material';

export function CRMPipelineBoard({ opportunities, stages, config }) {
  const colorScheme = config.get_color_scheme();
  const pipelineConfig = config.get_component_config().pipeline_board;

  const handleDragEnd = (result) => {
    // Handle opportunity stage change
    if (!result.destination) return;

    const { draggableId, destination } = result;
    updateOpportunityStage(draggableId, destination.droppableId);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Box sx={{ display: 'flex', gap: 2, overflowX: 'auto', pb: 2 }}>
        {stages.map(stage => (
          <Box key={stage.id} sx={{ minWidth: 300 }}>
            {/* Stage Header */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6" sx={{ mb: 1 }}>
                {stage.name}
              </Typography>

              {pipelineConfig.stage_summaries && (
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Chip
                    label={`${getStageOpportunities(stage.id).length} deals`}
                    size="small"
                  />
                  <Chip
                    label={`$${getStageValue(stage.id).toLocaleString()}`}
                    size="small"
                    sx={{ bgcolor: colorScheme[stage.id.toLowerCase()] + '20' }}
                  />
                </Box>
              )}
            </Box>

            {/* Droppable Stage Column */}
            <Droppable droppableId={stage.id}>
              {(provided, snapshot) => (
                <Box
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  sx={{
                    minHeight: 200,
                    bgcolor: snapshot.isDraggingOver ? 'grey.100' : 'transparent',
                    borderRadius: 1,
                    p: 1
                  }}
                >
                  {getStageOpportunities(stage.id).map((opportunity, index) => (
                    <Draggable
                      key={opportunity.id}
                      draggableId={opportunity.id}
                      index={index}
                    >
                      {(provided, snapshot) => (
                        <Card
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          sx={{
                            mb: 1,
                            p: 2,
                            cursor: 'pointer',
                            transform: snapshot.isDragging ? 'rotate(5deg)' : 'none',
                            boxShadow: snapshot.isDragging ? 4 : 1
                          }}
                        >
                          {/* Opportunity Card Content */}
                          <Typography variant="subtitle2" sx={{ mb: 1 }}>
                            {opportunity.title}
                          </Typography>

                          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            {opportunity.company}
                          </Typography>

                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Typography
                              variant="h6"
                              sx={{ color: colorScheme.priority_high }}
                            >
                              ${opportunity.value.toLocaleString()}
                            </Typography>

                            {pipelineConfig.probability_indicators && (
                              <Chip
                                label={`${opportunity.probability}%`}
                                size="small"
                                color={opportunity.probability >= 70 ? 'success' : 'default'}
                              />
                            )}
                          </Box>

                          <Typography variant="caption" color="text.secondary">
                            Expected close: {opportunity.expectedCloseDate}
                          </Typography>
                        </Card>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </Box>
              )}
            </Droppable>
          </Box>
        ))}
      </Box>
    </DragDropContext>
  );
}
"""
}